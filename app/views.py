from django.shortcuts import render, redirect
from django.views import View
from .utils import read_excel, find_enabled
from .models import Product

# Create your views here.


class AddProductsView(View):
    template = "add-products.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        excel_file = request.FILES.get("file-name", None)
        if excel_file is not None:
            df = read_excel(excel_file)
            row_iter = df.iterrows()
            objs = [
                Product(
                    item_code=row["Item Code"],
                    item_name=row["Item Name"],
                    category_l1=row["Category L1"],
                    category_l2=row["Category L2"],
                    upc=row["UPC"],
                    parent_code=row["Parent Code"],
                    price=row["MRP Price"],
                    size=row["Size"],
                    is_active=find_enabled(row["Enabled"]),
                )
                for index, row in row_iter
            ]
            Product.objects.bulk_create(objs)
        return redirect("app:productlist")


class ProductListView(View):
    template = "product-list.html"

    def get(self, request):
        items = Product.objects.all()
        active = len(items.filter(is_active=True))
        inactive = len(items.filter(is_active=False))
        context = {"items": items, "active": active, "inactive": inactive}
        return render(request, self.template, context)


class SearchView(View):
    template = "search.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        search_field = request.POST["search-field"]
        item_name = request.POST["name"]
        try:
            if search_field == "children":
                items = Product.get_children(item_name)
                context = {"items": items}
            if search_field == "parent":
                item = Product.objects.get(item_code=item_name)
                context = {"items": [item]}
        except Product.DoesNotExist:
            context = {"items": [item[0]]}
        except Product.MultipleObjectsReturned:
            context = {"items": [item[0]]}

        return render(request, self.template, context)
