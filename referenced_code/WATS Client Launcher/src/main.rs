// Copyright 2022-2022 Tauri Programme within The Commons Conservancy
// SPDX-License-Identifier: Apache-2.0
// SPDX-License-Identifier: MIT

#![allow(unused)]
#![windows_subsystem = "windows"]

use std::{any::Any, collections::HashMap, env, fs::File, io::{Read,Write}, path::{Path, PathBuf}, process::Command, fs::OpenOptions, os::windows::process::CommandExt};
use notify::{EventKind, RecursiveMode, Watcher};
use tao::{
    event::{ElementState, Event, WindowEvent}, event_loop::{ControlFlow, EventLoopBuilder}, platform::run_return::EventLoopExtRunReturn, window::Window
};
use tray_icon::{
    menu::{AboutMetadata, Menu, MenuEvent, MenuItem, PredefinedMenuItem}, TrayIcon, TrayIconBuilder, TrayIconEvent
};
//use log::{LevelFilter, Log, Metadata, Record};

use std::sync::Mutex;
use once_cell::sync::Lazy;
use chrono::{DateTime, Utc};

use std::fs;
use std::time::Duration;
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use widestring::U16CString;


use raw_window_handle::{HasWindowHandle, RawWindowHandle};
use std::sync::atomic::{AtomicPtr, Ordering};
use windows::{
    core::PCWSTR,
    Win32::Foundation::*,
    Win32::UI::WindowsAndMessaging::*,
};

static ORIGINAL_WNDPROC: AtomicPtr<std::ffi::c_void> = AtomicPtr::new(std::ptr::null_mut());

unsafe extern "system" fn custom_wnd_proc(
    hwnd: HWND,
    msg: u32,
    wparam: WPARAM,
    lparam: LPARAM,
) -> LRESULT {
    match msg {
        WM_QUERYENDSESSION | WM_ENDSESSION => {
            std::process::exit(0); // Exit the application
        }
        _ => {}
    }

    let original = ORIGINAL_WNDPROC.load(Ordering::Relaxed);
    CallWindowProcW(Some(std::mem::transmute(original)), hwnd, msg, wparam, lparam)
}

fn subclass_wndproc(window: &tao::window::Window) {
    if let Ok(RawWindowHandle::Win32(handle)) = window.window_handle().map(|h| h.as_raw()) {
        unsafe {
            let hwnd = HWND(handle.hwnd.get() as isize);
            let prev = SetWindowLongPtrW(hwnd, GWLP_WNDPROC, custom_wnd_proc as _);
            ORIGINAL_WNDPROC.store(prev as *mut _, Ordering::Relaxed);
        }
    }
}

// Simple logger struct with file writing capabilities
//struct SimpleLogger {
//    file: Mutex<std::fs::File>,
//    level: LevelFilter,
//}

//impl SimpleLogger {
//    // Helper function to log the current log level after initialization
//    fn log_startup_message(&self) {
//        let mut file = self.file.lock().unwrap();
//        writeln!(file, "[{}] [INFO] Logger initialized with level: {:?}", chrono::Utc::now().to_rfc3339_opts( chrono::SecondsFormat::Secs, true), self.level)
//            .expect("Failed to write startup log level");
//        }
//}

//// Implement the Log trait for SimpleLogger
//impl Log for SimpleLogger {
//    fn enabled(&self, metadata: &Metadata) -> bool {
//        metadata.level() <= self.level  // Only log messages at or below the set level
//    }

//    fn log(&self, record: &Record) {
//        if self.enabled(record.metadata()) {
//            let mut file = self.file.lock().unwrap();
//            writeln!(file, "[{}] [{}] {}", chrono::Utc::now().to_rfc3339_opts( chrono::SecondsFormat::Secs, true), record.level(), record.args()).unwrap();
//        }
//    }

//    fn flush(&self) {}
//}

//// Lazy static logger to defer initialization
//static LOGGER: Lazy<SimpleLogger> = Lazy::new(|| {
//    let mut log_level = log::LevelFilter::Info;
//    for arg in env::args().skip(1) {  // Skip the first arg (program name)
//        if arg.starts_with("-l"){
//            match arg.as_str() {
//                "-lT" => {log_level = log::LevelFilter::Trace;}
//                "-lD" => {log_level = log::LevelFilter::Debug;}
//                _ => { panic!("Invalid loglevel specified: {arg}. Use -lD for debug or -lT for trace, default log level is info");}
//            }
//        }
//    }

//    let log_file = get_program_data_path().join("watstray.log");

//    let logger = SimpleLogger {
//        file: Mutex::new(
//            OpenOptions::new()
//                .create(true)
//                .append(true)
//                .open(log_file)
//                .expect("Cannot open log file"),
//        ),
//        level: log_level,  // Set logging level here (Error, Warn, Info, Debug, Trace)
//    };
//    log::info!("loglevel: {log_level:?}");
//    logger.log_startup_message();
    
//    logger
//});

enum UserEvent {
    TrayIconEvent(tray_icon::TrayIconEvent),
    MenuEvent(tray_icon::menu::MenuEvent),
    FileWatchEvent(notify::Event)
}

#[derive(Debug, PartialEq, Eq, Hash)]
enum WATSExecutable{
    Configurator,
    ClientMonitor,
    YieldMonitor,
    PackageManager,
}

fn main() {
    //Logger::try_with_env_or_str("info").unwrap().start().unwrap();
    //env_logger::init();


    //log::set_logger(&*LOGGER)
    //    .map(|()| log::set_max_level(LOGGER.level))
    //    .expect("Failed to set logger");

    //log::trace!("WATS Launcher initializing");
    // TODO: Change ico path to runtime folder
    //let statusfile = concat!(env!("CARGO_MANIFEST_DIR"), "/src/clientstatus.txt");
    let exepath = get_executable_dir();
    let datapath = get_program_data_path();
    //let statusfilepath= exepath.join("clientstatus.txt");
    let statusfilepath = datapath.join("LauncherTooltip.txt");
    //let statusfilepath = exepath..push("clientstatus.txt"); //.join("clientstatus.txt").as_path();
    //log::trace!("WATS Launcher initializing");

    let iconmap = HashMap::from([
        ("online", "WBonline.ico"),
        ("offline", "WBoffline.ico"),
        ("error", "WBoffline.ico"),
    ]);

    // Lookup map for executable to launch
    let exemap = HashMap::from([
        (WATSExecutable::Configurator, "Virinco.WATS.Client.Configurator.exe"),
        (WATSExecutable::ClientMonitor, "Virinco.WATS.Client.StatusMonitor.exe"),
        (WATSExecutable::YieldMonitor, "Virinco.WATS.Client.YieldMonitor.exe"),
        (WATSExecutable::PackageManager, "Virinco.WATS.Client.PackageManager.exe"),
    ]);

    // Create the Tao event loop
    let event_loop = EventLoopBuilder::<UserEvent>::with_user_event().build();

    // Create a hidden dummy window to intercept Windows shutdown messages
    let hidden_window = tao::window::WindowBuilder::new()
        .with_visible(false)
        .build(&event_loop)
        .unwrap();
    subclass_wndproc(&hidden_window);

    // set a tray event handler that forwards the event and wakes up the event loop
    let proxy = event_loop.create_proxy();
    TrayIconEvent::set_event_handler(Some(move |event| {
        proxy.send_event(UserEvent::TrayIconEvent(event));
    }));

    // set a menu event handler that forwards the event and wakes up the event loop
    let proxy = event_loop.create_proxy();
    MenuEvent::set_event_handler(Some(move |event: MenuEvent| {
        proxy.send_event(UserEvent::MenuEvent(event));
    }));

    // Create eventloop-proxy for Filewatcher (notify::watcher)
    let fwproxy = event_loop.create_proxy();

    // Create watcher
    let mut watcher = notify::RecommendedWatcher::new(
        move |res| {
            if let Ok(event) = res {
                fwproxy
                    .send_event(UserEvent::FileWatchEvent(event));
            }
        }
        , notify::Config::default()).unwrap();
    
    // Start watcher on status file
    //let statusfilepath = std::path::Path::new(statusfile);
    watcher.watch(statusfilepath.as_path(), notify::RecursiveMode::NonRecursive).unwrap();
    //log::debug!("watching: {statusfilepath:?}");   // DEBUG output

    let tray_menu = Menu::new();

    let itm_cm = MenuItem::new("Open Client &Monitor", true, None);
    let itm_ym = MenuItem::new("Open &Yield Monitor", true, None);
    let itm_pm = MenuItem::new("Open &Package Manager", true, None);
    let itm_cfg = MenuItem::new("&Configure", true, None);
    let itm_exit = MenuItem::new("Exit", true, None);

    tray_menu.append_items(&[
        &itm_cm, &itm_ym, &itm_pm,
        &PredefinedMenuItem::separator(),
        &itm_cfg,
//        &PredefinedMenuItem::about(
//            None,
//            Some(AboutMetadata {
//                name: Some("WATS Client Launcher".to_string()),
//                copyright: Some("Copyright Virinco as".to_string()),
//                ..Default::default()
//            }),
//        ),
        &PredefinedMenuItem::separator(),
        &itm_exit
    ]);

    let mut tray_icon = None;

    let menu_channel = MenuEvent::receiver();
    let tray_channel = TrayIconEvent::receiver();

    //log::trace!("WATS Launcher initialized, starting event-loop");
    // Start the Tao event loop
    event_loop.run(move |event, _, control_flow| {
        *control_flow = ControlFlow::Wait;

        match event {
            Event::NewEvents(tao::event::StartCause::Init) => {
                // Initialize 
                let icopath = iconmap.get("offline").unwrap();
                let ico = tray_icon::Icon::from_path(*icopath, None).unwrap();

                tray_icon = Some(
                    TrayIconBuilder::new()
                        .with_menu(Box::new(tray_menu.clone()))
                        .with_tooltip("WATS Client Launcher - initializing")
                        .with_icon(ico)
                        .build()
                        .unwrap()
                );

                // Update tooltip status from statusfile
                if let Some(ti)=&tray_icon {
                    updatetrayicon(statusfilepath.as_path(), exepath.as_path(), &iconmap, &ti);
                };

                // We have to request a redraw here to have the icon actually show up.
                // Tao only exposes a redraw method on the Window so we use core-foundation directly.
                #[cfg(target_os = "macos")]
                unsafe {
                    use core_foundation::runloop::{CFRunLoopGetMain, CFRunLoopWakeUp};

                    let rl = CFRunLoopGetMain();
                    CFRunLoopWakeUp(rl);
                }
                //log::trace!("WATS Launcher initialization completed, event-loop running");

            }

            Event::MainEventsCleared =>{
                // Nothing to do here:
                //log::trace!("Event::MainEventsCleared - no actions");


            }
            Event::UserEvent(UserEvent::TrayIconEvent(event)) => {
                // Nothing to do here
                //log::trace!("Event::UserEvent::TrayIconEvent: {event:?}");

            }
            
            Event::UserEvent(UserEvent::FileWatchEvent(event)) => {
                //log::trace!("Event::UserEvent::FileWatchEvent : {event:?}");
                // Status file changed - update icon and tooltip
                if let Some(ti)=&tray_icon {
                    updatetrayicon(statusfilepath.as_path(), exepath.as_path(), &iconmap, &ti);
                }

            }
            
            Event::UserEvent(UserEvent::MenuEvent(event)) => {
                // Menu event, check for item-click and perform operation
                //log::trace!("Event::UserEvent::MenuEvent: {event:?}");
                if event.id == itm_cm.id() {
                    // Start Client Monitor
                    if let Some(exename) = exemap.get(&WATSExecutable::ClientMonitor){
                        spawnprocess(exepath.join(&exename).as_path(), "", false);    
                    }
                    //else {log::warn!("Unable to find executable-filename for ClientMonitor")}
                }
                if event.id == itm_ym.id() {
                    // Start Yield Monitor
                    if let Some(exename) = exemap.get(&WATSExecutable::YieldMonitor){
                        spawnprocess(exepath.join(&exename).as_path(), "", false);    
                    }
                    //else {log::warn!("Unable to find executable-filename for YieldMonitor")}
                }
                if event.id == itm_pm.id() {
                    
                    //log::warn!("Starting PackageManager");
                    // Start Package Manager
                    if let Some(exename) = exemap.get(&WATSExecutable::PackageManager){
                        let t = exepath.join(&exename);
                        //spawn_or_focus_package_manager(&exepath, "");
                        spawnprocess(exepath.join(&exename).as_path(), "", false);    

                    }
                    //else {log::warn!("Unable to find executable-filename for PackageManager")}
                }
                if event.id == itm_cfg.id() {
                    // Start Configurator
                    if let Some(exename) = exemap.get(&WATSExecutable::Configurator){
                        spawnprocess(exepath.join(&exename).as_path(), "", true);    
                    }
                    //else {log::warn!("Unable to find executable-filename for Configurator")}
                }

                if event.id == itm_exit.id() {
                    tray_icon.take();
                    //log::info!("User initiated exit");
                    *control_flow = ControlFlow::Exit;
                }
            }
            
            Event::UserEvent(subevent) =>{
                // Nothing to do here
                //log::trace!("Event::UserEvent::UserEvent : unknown event");
                //print_type_of(&subevent);

            }
            
            _ => {
                //log::trace!("Event: other-unknown-event:");
                //print_type_of(&event);

            }
        }
    });

}

/// Set tray-icon using iconpath
fn seticon(tray_icon: &TrayIcon, iconpath: &Path ){
    let icon = tray_icon::Icon::from_path(iconpath, None).unwrap();
    tray_icon.set_icon(Some(icon));
}

fn spawnprocess(path: &Path, arguments: &str, run_as_admin: bool) {
    let path = path.to_path_buf(); // Convert `&Path` to `PathBuf` (owned)
    let arguments = arguments.to_string(); // Convert `&str` to `String` (owned)

    let mut command = Command::new(&path);

    // Only split and add arguments if not empty
    if !arguments.trim().is_empty() {
        command.args(arguments.split_whitespace());
    }

    // Set working directory to the .exe's directory
    if let Some(parent) = path.parent() {
        command.current_dir(parent);
    }
    if run_as_admin {
        // Use ShellExecute via "runas" verb
        let args: Vec<&str> = arguments.split_whitespace().collect();

        match runas::Command::new(&path)
            .args(&args)
            .status()
        {
            Ok(status) => {},
            Err(e) => {},
        }
    }
    else 
    {
        match command.spawn() {
            Ok(mut child) => {
                //log::debug!("Successfully started process: {path:?} {arguments}");
                // Spawn a thread to wait for the process to finish
                std::thread::spawn(move || {
                    if let Err(e) = child.wait() {
                        //log::warn!("Failed to wait for process {path:?} {arguments}: {e}");
                    }
                });
            }
            Err(e) => {
                //log::warn!("Failed to spawn process {path:?} {arguments}: {e}");
            }
        }
    }
}

fn to_pcwstr(s: &str) -> PCWSTR {
    let wide: Vec<u16> = OsStr::new(s).encode_wide().chain(Some(0)).collect();
    PCWSTR(wide.as_ptr())
}

fn bring_existing_window_to_front(class_name: &str, window_title: &str) {
    unsafe {
        let hwnd: HWND = FindWindowW(to_pcwstr(class_name), to_pcwstr(window_title));
        if hwnd.0 != 0 {
            ShowWindow(hwnd, SW_RESTORE);
            SetForegroundWindow(hwnd);
        }
    }
}

fn is_process_running(exe_name: &str) -> bool {
    let output = Command::new("tasklist")
        .arg("/FI")
        .arg(format!("IMAGENAME eq {}", exe_name))
        .output()
        .expect("Failed to execute tasklist");

    let output_str = String::from_utf8_lossy(&output.stdout);
    output_str.contains(exe_name)
}

fn spawn_or_focus_package_manager(exepath: &std::path::Path, exename: &str) {
    if is_process_running(exename) {
        // Replace with the actual class name and window title if known
        bring_existing_window_to_front("WindowClass", "WATS Package Manager");
    } else {
        let _ = Command::new(exepath.join(exename))
            .spawn()
            .expect("Failed to launch Package Manager");
    }
}



fn parse_statusfile(statusfilecontents: &str) -> (HashMap<String, &str>, String) {
    // Separate hash-lines from other text
    let mut hash_lines = HashMap::new();
    let mut other_lines = Vec::new();

    for line in statusfilecontents.lines() {
        if line.starts_with('#') {
            let kv = line[1..].split_once(":").unwrap();
            hash_lines.insert(kv.0.trim().to_lowercase(), kv.1.trim());
        } else {
            other_lines.push(line.to_string());
        }
    }
    let mut stext=other_lines.join("\n");
    (hash_lines, stext)
}

fn updatetrayicon(statusfilepath: &Path, exepath: &Path, iconmap: &HashMap<&str,&str>, ti: &TrayIcon){
    //log::trace!("Statusfile reload");
    // Load statusfile 
    //TBD/TODO: Handle missing file without panicing?
    let mut file = File::open(statusfilepath).expect("Unable to open file");
    let mut contents = String::new();
    //TBD/TODO: Handle read-error  file without panicing?
    let len: usize = file.read_to_string(&mut contents).expect("Unable to read file");
    // Parse statusfile content:
    let (kv, stext) = parse_statusfile(&contents);
    //log::debug!("Setting tooltip from statusfile:\n{}", stext);
    // Update tooltip from statusfile
    ti.set_tooltip( Some(stext));
    // Update icon from #Icon-value
    if let Some(value) = kv.get("icon"){
        let iv = (*value).to_lowercase();
        if let Some(icopath) = iconmap.get(iv.as_str()){
            seticon(ti, exepath.join(&icopath).as_path());
            //log::debug!("Setting icon statusfile:\n{icopath}");
        }else{
            // specified icon-value in statusfile is not recognized
            //log::warn!("seticon: Invalid status-code:{iv}");
            //TBD: Set meaningful Error code/icon/tooltip? (ie. )
        }
    }
    else{
        // No icon-value found in statusfile, setting error status/icon
        //log::warn!("seticon: no status-code (icon) found in status file, setting error");
        if let Some(icopath) = iconmap.get("error"){
            seticon(ti, exepath.join(&icopath).as_path());
        }
        //iconmap error-key must always exist - no need to handle else here...
    }
}

/// Get folder of the executable as a PathBuf
fn get_executable_dir() -> PathBuf {
    //TBD/TODO: Handle failed to get exepath and/or "no parent dir"?
    env::current_exe()
        .expect("Failed to get current executable path")
        .parent()
        .expect("Executable has no parent directory")
        .to_path_buf()
}

fn get_program_data_path() -> PathBuf {
    let base = env::var_os("PROGRAMDATA")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from(r"C:\ProgramData")); // Fallback if env var is missing

    base.join("Virinco").join("WATS").to_path_buf()
}
