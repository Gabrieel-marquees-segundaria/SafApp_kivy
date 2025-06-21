from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass, cast
from android import activity

# Classes Java usadas
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

REQUEST_CODE = 12345

class SAFApp(App):
    def build(self):
        self.activity = PythonActivity.mActivity
        self.ctx = self.activity.getApplicationContext()
        self.label = Label(text="Nenhuma pasta selecionada")
        btn_select = Button(text="Selecionar pasta")
        btn_select.bind(on_press=lambda _: self.select_folder())
        btn_save = Button(text="Salvar arquivo")
        btn_save.bind(on_press=lambda _: self.save_file())
        btn_load = Button(text="Ler arquivo")
        btn_load.bind(on_press=lambda _: self.load_file())

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(btn_select)
        layout.add_widget(btn_save)
        layout.add_widget(btn_load)

        activity.bind(on_activity_result=self.on_activity_result)
        return layout

    def select_folder(self):
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        self.activity.startActivityForResult(intent, REQUEST_CODE)

    def on_activity_result(self, requestCode, resultCode, data):
        if requestCode != REQUEST_CODE:
            return
        if resultCode != self.activity.RESULT_OK:
            self.label.text = "Seleção cancelada"
            return
        uri = data.getData()
        self.activity.getContentResolver().takePersistableUriPermission(
            uri,
            Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
        )
        self.folderUri = uri
        self.label.text = f"Pasta selecionada: {uri.toString()}"

    def save_file(self):
        if not hasattr(self, 'folderUri'):
            self.label.text = "Selecione a pasta antes!"
            return
        # Vamos criar um arquivo chamado exemplo.txt com conteúdo simples
        DocumentFile = autoclass('androidx.documentfile.provider.DocumentFile')
        docFolder = DocumentFile.fromTreeUri(self.ctx, self.folderUri)
        newFile = docFolder.createFile("text/plain", "exemplo.txt")
        fos = self.activity.getContentResolver().openOutputStream(newFile.getUri())
        fos.write("Olá do Kivy via SAF!".encode('utf-8'))
        fos.close()
        self.label.text = "Arquivo salvo: exemplo.txt"

    def load_file(self):
        if not hasattr(self, 'folderUri'):
            self.label.text = "Selecione a pasta antes!"
            return
        DocumentFile = autoclass('androidx.documentfile.provider.DocumentFile')
        docFolder = DocumentFile.fromTreeUri(self.ctx, self.folderUri)
        for f in docFolder.listFiles().toArray():
            if f.getName() == "exemplo.txt":
                fis = self.activity.getContentResolver().openInputStream(f.getUri())
                data = b""
                buf = bytearray(1024)
                while True:
                    r = fis.read(buf)
                    if r == -1:
                        break
                    data += buf[:r]
                fis.close()
                self.label.text = "Conteúdo: " + data.decode('utf-8')
                return
        self.label.text = "Arquivo exemplo.txt não encontrado"

if __name__ == '__main__':
    SAFApp().run()
