from gi.repository import Nemo, GObject
import dbus
import urllib
import os
import gettext
import locale


(
    CORE_INITIALIZING,
    CORE_AUTHORIZING,
    CORE_WAITING,
    CORE_SYNCING,
    CORE_READY,
    CORE_PAUSED,
    CORE_ERROR,
    CORE_SELECTIVE_SYNC,
    CORE_RESTARTING,
    CORE_OFFLINE
) = xrange(0, 10)


def init_localization():
    '''prepare l10n'''
    locale.setlocale(locale.LC_ALL, '')
    loc = locale.getlocale()
    filename = "meocloud_mo/%s.mo" % locale.getlocale()[0][0:2]
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

    try:
        trans = gettext.GNUTranslations(open(path, "rb"))
    except IOError:
        trans = gettext.NullTranslations()

    trans.install()


class MEOCloudNemo(Nemo.InfoProvider, Nemo.MenuProvider,
                       GObject.GObject):
    def __init__(self):
        init_localization()
        bus = dbus.SessionBus()
        self.service = None
        self.get_dbus()

    def get_dbus(self):
        if self.service is None:
            bus = dbus.SessionBus()

            try:
                self.service = bus.get_object('pt.meocloud.dbus',
                                              '/pt/meocloud/dbus')

                self.status = self.service.get_dbus_method(
                    'Status', 'pt.meocloud.dbus')
                self.file_in_cloud = self.service.get_dbus_method(
                    'FileInCloud', 'pt.meocloud.dbus')
                self.get_cloud_home = self.service.get_dbus_method(
                    'GetCloudHome', 'pt.meocloud.dbus')
                self.share_link = self.service.get_dbus_method(
                    'ShareLink', 'pt.meocloud.dbus')
                self.share_folder = self.service.get_dbus_method(
                    'ShareFolder', 'pt.meocloud.dbus')
                self.open_in_browser = self.service.get_dbus_method(
                    'OpenInBrowser', 'pt.meocloud.dbus')
            except:
                pass

    def get_local_path(self, path):
        return urllib.unquote(path)[7:]

    def valid_uri(self, uri):
        if not uri.startswith("file://"):
            return False
        else:
            return True

    def update_file_info(self, item):
        self.get_dbus()
        uri = item.get_uri()

        if self.valid_uri(uri):
            uri = self.get_local_path(uri)

            try:
                if uri == self.get_cloud_home():
                    status = self.status()

                    if (status == CORE_INITIALIZING or
                            status == CORE_AUTHORIZING or
                            status == CORE_WAITING):
                        item.add_emblem("emblem-synchronizing-symbolic")
                    elif status == CORE_SYNCING:
                        item.add_emblem("emblem-synchronizing-symbolic")
                    elif status == CORE_READY:
                        item.add_emblem("emblem-ok-symbolic")
                else:
                    in_cloud, syncing = self.file_in_cloud(uri)
                    if in_cloud and syncing:
                        item.add_emblem("emblem-synchronizing-symbolic")
                    elif in_cloud:
                        item.add_emblem("emblem-ok-symbolic")
            except:
                self.service = None
                pass

        return Nemo.OperationResult.COMPLETE

    def get_file_items(self, window, files):
        if len(files) != 1:
            return None,

        self.get_dbus()
        item = files[0]
        uri = item.get_uri()

        if self.valid_uri(uri):
            uri = self.get_local_path(uri)

            try:
                in_cloud, syncing = self.file_in_cloud(uri)
                if not in_cloud:
                    return None,
            except:
                self.service = None
                return None,
        else:
            return None,

        top_menuitem = Nemo.MenuItem.new('MEOCloudMenuProvider::MEOCloud',
                                             'MEO Cloud', '', '')

        submenu = Nemo.Menu()
        top_menuitem.set_submenu(submenu)

        if os.path.isfile(uri):
            link_menuitem = Nemo.MenuItem.new('MEOCloudMenuProvider::Copy',
                                                  _('Copy Link'), '', '')
            link_menuitem.connect("activate", lambda w: self.share_link(uri))
            submenu.append_item(link_menuitem)
        else:
            share_menuitem = Nemo.MenuItem.new(
                'MEOCloudMenuProvider::Share', _('Share Folder'), '', '')
            share_menuitem.connect("activate", lambda w:
                                   self.share_folder(uri))
            submenu.append_item(share_menuitem)

        browser_menuitem = Nemo.MenuItem.new(
            'MEOCloudMenuProvider::Browser', _('Open in Browser'), '', '')
        browser_menuitem.connect("activate", lambda w:
                                 self.open_in_browser(uri))
        submenu.append_item(browser_menuitem)

        return top_menuitem,

    def get_background_items(self, window, item):
        return None,