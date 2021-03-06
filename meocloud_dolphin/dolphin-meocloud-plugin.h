#ifndef DolphinMEOCloudPlugin_H
#define DolphinMEOCloudPlugin_H

#include <kversioncontrolplugin.h>
#include <kabstractfileitemactionplugin.h>
#include <QtCore/QDateTime>
#include <QtCore/QHash>
#include <QtCore/QVariantList>
#include <QtCore/QFileInfo>
#include <QtCore/QTimer>
#include <QLocalSocket>

#define BUFSIZE 8192

class DolphinMEOCloudPlugin : public KVersionControlPlugin
{
    Q_OBJECT

public:
    DolphinMEOCloudPlugin(QObject *parent = 0, const QVariantList &args = QVariantList());
    virtual ~DolphinMEOCloudPlugin();
    virtual QString fileName() const;
    virtual bool beginRetrieval(const QString &directory);
    virtual void endRetrieval();
    virtual KVersionControlPlugin::VersionState versionState(const KFileItem &item);
    virtual QList<QAction *>contextMenuActions(const KFileItemList &items);
    virtual QList<QAction *>contextMenuActions(const QString &directory);

public slots:
    void setVersionState();

    void subscribe();
    void requestStatus(QString path);

    void socket_connected();
    void socket_disconnected();

    void socket_readReady();
    void socket_error(QLocalSocket::LocalSocketError);

    void reloadConfig();
private slots:
    void shareFolderAction();
    void openInBrowserAction();
    void shareFileLinkAction();

private:
    QList<QAction *>getActions(QString url, bool isDir);

    QAction *m_shareFolderAction;
    QAction *m_openInBrowserAction;
    QAction *m_shareFileLinkAction;

    void processData(QString data);

    void requestLink(QString path);
    void requestShare(QString path);
    void requestOpen(QString path);
    void setCloudParent(void);

    QString m_cloudDir;
    QString m_cloudParentDir;
    QString m_lastDir;
    QString m_contextUrl;
    QHash<QString, KVersionControlPlugin::VersionState> m_versionInfoHash;

    QLocalSocket*   m_socket;
    QString m_message;
    char m_rawbuffer[BUFSIZE];
    QString m_buffer;
};
#endif // DolphinMEOCloudPlugin_H
