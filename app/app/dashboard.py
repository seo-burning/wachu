"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'app.dashboard.CustomIndexDashboard'
"""

# https://github.com/sehmaschine/django-grappelli

from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Store',
            column=1,
            models=('store.models.Store', 'store.models.StorePost')
        ))
        self.children.append(modules.ModelList(
            title='Product',
            column=1,
            models=('product.models.Product',)
        ))

        self.children.append(modules.ModelList(
            title='Publish _ Post(HOME)',
            column=1,
            models=('publish.models.LinkingBanner',
                    'publish.models.BannerPublish',
                    'publish.models.PostTagGroup',
                    'publish.models.MainPagePublish',
                    )
        ))
        self.children.append(modules.ModelList(
            title='Publish _ Magazine',
            column=1,
            models=('publish.models.PostGroup',
                    'publish.models.MagazinePublish',
                    )
        ))
        self.children.append(modules.ModelList(
            title='Advertisement',
            column=1,
            models=('advertisement.models.ProductRecommendKeyword',
                    )
        ))

        self.children.append(modules.ModelList(
            title='Users',
            column=2,
            models=('core.models.User', 'core.models.UserPushToken',)
        ))

        self.children.append(modules.ModelList(
            title='Notification',
            column=2,
            models=('core.models.Notice',)
        ))
        self.children.append(modules.LinkList(
            layout='inline',
            column=2,
            children=(
                ['Facebook', 'https://www.facebook.com/pg/dabivn/',
                 True,
                 ],
                ['Instagram', 'https://www.instagram.com/dabi.vn/', True],
            )
        ))
        self.children.append(modules.AppList(
            _('AppList: All'),
            collapsible=True,
            column=3,
            css_classes=('collapse grp-closed',),
            exclude=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=3,
            collapsible=False,
            limit=5,
        ))
