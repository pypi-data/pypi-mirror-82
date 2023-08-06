import QtQuick
import QtQuick.Controls 2.15

Page {
    width: 960
    height: 500

    header: Label {
        color: "#FFFFFF"
        text: qsTr("List")
        font.pointSize: 17
        font.bold: true
        font.family: "Arial"
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        padding: 1
    }
    Rectangle {
        id: root
        width: parent.width
        height: parent.height

        Image {
            id: image
            fillMode: Image.PreserveAspectCrop
            anchors.centerIn: root
            source: "/mark/MarkPy/markipy/gui/resource/earth.960x540.jpg"
            opacity: 1
        }

        ListView {
            id: list_view
            anchors.fill: root
            anchors.margins: 25
            model: myModel
            delegate: Text {
                color: "#0080FF"
                anchors.leftMargin: 70
                font.pointSize: 16
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                text: display
                 MouseArea {
                    anchors.fill: parent
                    onClicked: list_view.currentIndex = index
                 }
            }
            highlight: Rectangle {
            color: '#DCE7FA'
            }
            focus: true
            onCurrentIndexChanged: {
            var x = myListControl.add_item_selected(list_view.currentIndex)
            console.log(x)
            console.log(list_view.currentIndex)
            }
        }
    }
    NumberAnimation {
        id: anim
        running: true
        target: list_view
        property: "contentY"
        duration: 1
    }
}
