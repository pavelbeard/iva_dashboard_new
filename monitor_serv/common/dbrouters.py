from django.conf import settings

DEBUG = settings.DEBUG


class BaseDBRouter:
    """Базовый класс для машрутизаторов баз данных"""
    router_app_labels: set = {}

    def db_for_read(self, model, **hints):
        """
        Попытка прочитать модели, которые находятся в приложениях, указанных в router_app_labels
        в БД, указанную в возврате метода.
        """
        pass

    def db_for_write(self, model, **hints):
        """
        Попытка записать модели, которые находятся в приложениях, указанных в router_app_labels
        в БД, указанную в возврате метода.
        """
        pass

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешает отношения, если модели, указанные в router_app_labels - вовлечены
        """
        pass

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Убедись, что приложения содержатся в БД
        """
        pass


class IvaDashboardRouter(BaseDBRouter):
    router_app_labels = {'auth', 'admin', 'contenttype', 'dashboard', 'dashboard_users'}

    def db_for_read(self, model, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "iva_dashboard"

        if model._meta.app_label in self.router_app_labels:
            return __db

        return None

    def db_for_write(self, model, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "iva_dashboard"

        if model._meta.app_label in self.router_app_labels:
            return __db

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.router_app_labels or \
                obj2._meta.app_label in self.router_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "iva_dashboard"

        if app_label in self.router_app_labels:
            return db == __db


class IvcsRouter(BaseDBRouter):
    router_app_labels = {'dashboard_ivcs', 'dashboard_ivcs_detail'}

    def db_for_read(self, model, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "ivcs"

        if model._meta.app_label in self.router_app_labels:
            return __db

        return None

    def db_for_write(self, model, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "ivcs"

        if model._meta.app_label in self.router_app_labels:
            return __db

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.router_app_labels or \
                obj2._meta.app_label in self.router_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # __db = "test_db" if DEBUG else "iva_dashboard"
        __db = "ivcs"

        if app_label in self.router_app_labels:
            return db == __db



