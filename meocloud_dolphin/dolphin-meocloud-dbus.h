/*
 * This file was generated by qdbusxml2cpp version 0.7
 * Command line was: qdbusxml2cpp pt.meocloud.shell.xml -a ShellBus
 *
 * qdbusxml2cpp is Copyright (C) 2012 Digia Plc and/or its subsidiary(-ies).
 *
 * This is an auto-generated file.
 * This file may have been hand-edited. Look for HAND-EDIT comments
 * before re-generating it.
 */

#ifndef SHELLBUS_H_1396017396
#define SHELLBUS_H_1396017396

#include <QtCore/QObject>
#include <QtDBus/QtDBus>
class QByteArray;
template<class T> class QList;
template<class Key, class Value> class QMap;
class QString;
class QStringList;
class QVariant;

/*
 * Adaptor class for interface pt.meocloud.shell
 */
class ShellAdaptor: public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "pt.meocloud.shell")
    Q_CLASSINFO("D-Bus Introspection", ""
"  <interface name=\"pt.meocloud.shell\">\n"
"    <method name=\"UpdateFile\">\n"
"      <arg direction=\"in\" type=\"s\" name=\"path\"/>\n"
"    </method>\n"
"  </interface>\n"
        "")
public:
    ShellAdaptor(QObject *parent);
    virtual ~ShellAdaptor();

public: // PROPERTIES
public Q_SLOTS: // METHODS
    void UpdateFile(const QString &path);
Q_SIGNALS: // SIGNALS
};

class ShellServer : public QObject
{
    Q_OBJECT
public:
    explicit ShellServer(QObject *parent = 0):
        QObject(parent)
    {
    }

public slots:
    void UpdateFile(const QString &path)
    {
        QMetaObject::invokeMethod(parent(), "setVersionState");
    }
signals:
    void responseFromServer(const QString &data);
};

#endif
