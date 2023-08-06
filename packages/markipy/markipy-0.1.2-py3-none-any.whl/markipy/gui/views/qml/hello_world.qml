import QtQuick 2.5

Rectangle {
    id: page
    width: 320; height: 480
    color: "lightgrey"

    Text {
        id: helloText
        text: "Hello World!"
        y: 30
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 24
        font.bold: true
    }
}