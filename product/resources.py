from import_export import resources
from .models import ArticleImage

class ArticleImageResource(resources.ModelResource):
    class Meta:
        model = ArticleImage

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=True, **kwargs):
        print(dataset)