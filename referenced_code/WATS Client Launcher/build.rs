extern crate embed_resource;

fn main() {
    //embed_resource::compile("tray-example.rc", embed_resource::NONE);
    std::env::set_var("WINDRES", "\"C:\\msys64\\mingw64\\bin\\windres.exe\"");
    embed_resource::compile("icons.rc", embed_resource::NONE);
}
