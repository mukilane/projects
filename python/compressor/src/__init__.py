import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import brotli
import os.path


class Compressor(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Compressor")
        self.set_border_width(16)
        self.set_resizable(False)
        self.set_icon_from_file("../icon.png")

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Compressor"
        self.set_titlebar(hb)

        # Main Container
        self.containerBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.containerBox.set_hexpand(True)
        self.containerBox.set_vexpand(True)
        self.add(self.containerBox)

        # Stack and Stack Switcher
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_hexpand(True)
        stack_switcher.set_stack(stack)

        self.containerBox.pack_start(stack_switcher, False, False, 0)
        self.containerBox.pack_start(stack, False, False, 0)

        # Compression
        compressBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        stack.add_titled(compressBox, "compress", "Compression")

        cbInner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        compressBox.pack_start(cbInner, False, False, 0)

        Cactionbar = Gtk.ActionBar()
        Cactionbar.set_hexpand(True)
        compressBox.pack_end(Cactionbar, False, False, 0)

        self.compressSelectBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cbInner.pack_start(self.compressSelectBox, False, False, 0)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        cbInner.pack_start(separator, False, False, 0)

        self.compressParamsBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cbInner.pack_start(self.compressParamsBox, False, False, 0)

        inputFileLabel = Gtk.Label("Select the file to compress")
        self.compressSelectBox.pack_start(inputFileLabel, False, False, 0)
        self.inputFileChooserForCompress = Gtk.FileChooserButton(
            title="Select a file to compress")
        self.inputFileChooserForCompress.connect(
            "file-set", self.file_selected)
        self.compressSelectBox.pack_start(
            self.inputFileChooserForCompress, False, False, 0)

        outputLocationLabel = Gtk.Label("Select the output location")
        self.compressSelectBox.pack_start(outputLocationLabel, False, False, 0)
        self.outputLocationChooserForCompress = Gtk.FileChooserButton(
            title="Select a location", action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.outputLocationChooserForCompress.connect(
            "file-set", self.folder_selected)
        self.compressSelectBox.pack_start(
            self.outputLocationChooserForCompress, False, False, 0)

        adjustment = Gtk.Adjustment(5, 0, 11, 0, 0, 0)
        sliderLabel = Gtk.Label("Select Compression Level")
        self.compressParamsBox.pack_start(sliderLabel, False, False, 0)
        self.slider = Gtk.SpinButton.new_with_range(min=0, max=11, step=1)
        self.slider.set_value(11)
        self.compressParamsBox.pack_start(self.slider, False, False, 0)

        modeLabel = Gtk.Label("Select Mode")
        modeLabel.set_justify(Gtk.Justification.LEFT)
        self.compressParamsBox.pack_start(modeLabel, False, False, 0)
        radio_mode = Gtk.RadioButton(label="Generic")
        radio_mode.connect("toggled", self.mode_checked)
        self.compressParamsBox.pack_start(radio_mode, False, False, 0)
        radio_text = Gtk.RadioButton(label="Text", group=radio_mode)
        radio_text.connect("toggled", self.mode_checked)
        self.compressParamsBox.pack_start(radio_text, False, False, 0)
        radio_font = Gtk.RadioButton(label="Font", group=radio_mode)
        radio_font.connect("toggled", self.mode_checked)
        self.compressParamsBox.pack_start(radio_font, False, False, 0)

        compressButton = Gtk.Button("Compress")
        compressButton.connect("clicked", self.compress)
        Cactionbar.pack_end(compressButton)

        # Decompression
        decompressBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=16)
        stack.add_titled(decompressBox, "decompress", "Decompression")

        dbInner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        decompressBox.pack_start(dbInner, False, False, 0)

        Dactionbar = Gtk.ActionBar()
        Dactionbar.set_hexpand(True)
        decompressBox.pack_end(Dactionbar, False, False, 0)

        self.decompressSelectBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8)
        dbInner.pack_start(self.decompressSelectBox, False, False, 0)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        dbInner.pack_start(separator, False, False, 0)

        self.decompressParamsBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8)
        dbInner.pack_start(self.decompressParamsBox, False, False, 0)

        inputFileLabelDecompress = Gtk.Label("Select the file to decompress")
        self.decompressSelectBox.pack_start(
            inputFileLabelDecompress, False, False, 0)
        self.inputFileChooserForDecompress = Gtk.Button("Select")
        self.inputFileChooserForDecompress.connect(
            "clicked", self.select_br_file)
        self.decompressSelectBox.pack_start(
            self.inputFileChooserForDecompress, False, False, 0)

        outputLocationLabelDecompress = Gtk.Label("Select the output location")
        self.decompressSelectBox.pack_start(
            outputLocationLabelDecompress, False, False, 0)
        self.outputLocationChooserForDecompress = Gtk.FileChooserButton(
            title="Select a location", action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.outputLocationChooserForDecompress.connect(
            "file-set", self.folder_selected)
        self.decompressSelectBox.pack_start(
            self.outputLocationChooserForDecompress, False, False, 0)

        decompressButton = Gtk.Button("Decompress")
        decompressButton.connect("clicked", self.decompress)
        Dactionbar.pack_end(decompressButton)

        self.file = ""
        self.out = ""
        self.mode = 0

    def file_selected(self, filechooserbutton):
        self.file = filechooserbutton.get_filename()
        filename = os.path.basename(self.file)
        self.filename = filename

    def folder_selected(self, folderchooserbutton):
        out_folder = folderchooserbutton.get_uri()
        self.out = out_folder[7:] + '/'

    def mode_checked(self, radiobutton):
        if radiobutton.get_active():
            label = radiobutton.get_label()
            if label == 'Generic':
                self.mode = 0
            elif label == 'Text':
                self.mode = 1
            elif label == 'Font':
                self.mode = 2

    def select_br_file(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file to decompress", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file = dialog.get_filename()
            self.filename = os.path.basename(self.file)
        dialog.destroy()

    def add_filters(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Brotli files")
        filter_py.add_pattern("*.br")
        dialog.add_filter(filter_py)

    def compress(self, widget):
        quality = self.slider.get_value_as_int()
        file = self.file
        self.out = self.out + self.filename + '.br'
        with open(file, 'rb') as infile:
            filedata = infile.read()
        data = brotli.compress(
            filedata,
            mode=self.mode,
            quality=quality,
            lgwin=22,
            lgblock=0)
        outfile = open(self.out, 'wb')
        outfile.write(data)
        outfile.close()

    def decompress(self, widget):
        dest_filename = self.filename.split('.')[:-1]
        dest_filename = '.'.join(dest_filename)
        self.out = self.out + dest_filename
        file = self.file
        with open(file, 'rb') as infile:
            filedata = infile.read()
        data = brotli.decompress(filedata)
        outfile = open(self.out, 'wb')
        outfile.write(data)
        outfile.close()


css = b"""
window.background {
    background: #eee;
}
headerbar, headerbar button { 
    background: #fb8c00;
    color: black;
}
button {
    background: #fafafa;
    color: black;
}
button:active, button:checked {
    background: #fb8c00;
    color: white;
}
checkbutton:checked {
  background: #fb8c00;
}
spinbutton {
    background: #fafafa;
    color: black;
}
label {
    color: #111;
}
"""
style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER
)

win = Compressor()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
