#!/usr/bin/env python3
from pathlib import Path
import json
import plistlib
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-location-storage-baseline.md"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def parse_xml(relative_path, failures):
    try:
        ET.parse(ROOT / relative_path)
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_json(relative_path, failures):
    try:
        json.loads(read(relative_path))
    except json.JSONDecodeError as error:
        failures.append(f"{relative_path} is not valid JSON: {error}")


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def check_png(relative_path, failures):
    path = ROOT / relative_path
    with path.open("rb") as file:
        signature = file.read(len(PNG_SIGNATURE))
    require(signature == PNG_SIGNATURE, f"{relative_path} must be a PNG image", failures)
    require(path.stat().st_size > 100, f"{relative_path} must not be empty", failures)


def git_ls_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.splitlines()


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "Route.gpx",
        "docs/plans/2026-06-08-location-storage-baseline.md",
        "docs/plans/2026-06-08-location-manager-delegate-setup.md",
        "docs/plans/2026-06-08-location-notification-main-thread.md",
        "docs/plans/2026-06-08-notification-observer-lifecycle.md",
        "docs/readme-overview.svg",
        "scripts/check-baseline.py",
        "Journal/Info.plist",
        "Journal/LocationsStorage.swift",
        "Journal/Location.swift",
        "Journal/MapViewController.swift",
        "Journal/PlacesTableViewController.swift",
        "Journal/AppDelegate.swift",
        "Journal/Base.lproj/Main.storyboard",
        "Journal/LaunchScreen.storyboard",
        "Journal/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "Journal/Assets.xcassets/rw-logo.imageset/Razewarelogo_1024.png",
        "Journal.xcodeproj/project.pbxproj",
        "Journal.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "Journal.xcodeproj/project.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist",
    ]
    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "docs/readme-overview.svg",
        "Route.gpx",
        "Journal/Base.lproj/Main.storyboard",
        "Journal/LaunchScreen.storyboard",
        "Journal.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "Journal.xcodeproj/project.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist",
    ]:
        parse_xml(xml_file, failures)

    for json_file in [
        "Journal/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "Journal/Assets.xcassets/rw-logo.imageset/Contents.json",
        "Journal/Assets.xcassets/recents.imageset/Contents.json",
        "Journal/Assets.xcassets/search.imageset/Contents.json",
    ]:
        parse_json(json_file, failures)

    for image_file in [
        "Journal/Assets.xcassets/AppIcon.appiconset/Icon1024.png",
        "Journal/Assets.xcassets/rw-logo.imageset/Razewarelogo_1024.png",
        "Journal/Assets.xcassets/recents.imageset/TabBar_MostRecent_2x.png",
        "Journal/Assets.xcassets/search.imageset/TabBar_Search_2x.png",
    ]:
        check_png(image_file, failures)

    app_plist = parse_plist("Journal/Info.plist", failures)
    project = read("Journal.xcodeproj/project.pbxproj")
    storage = read("Journal/LocationsStorage.swift")
    map_controller = read("Journal/MapViewController.swift")
    places_controller = read("Journal/PlacesTableViewController.swift")
    app_delegate = read("Journal/AppDelegate.swift")
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    delegate_plan_path = ROOT / "docs/plans/2026-06-08-location-manager-delegate-setup.md"
    delegate_plan = delegate_plan_path.read_text(encoding="utf-8") if delegate_plan_path.exists() else ""
    main_thread_plan = read("docs/plans/2026-06-08-location-notification-main-thread.md")
    notification_plan = read("docs/plans/2026-06-08-notification-observer-lifecycle.md")
    tracked = git_ls_files()

    require("NSLocationAlwaysAndWhenInUseUsageDescription" in app_plist,
            "Info.plist must document always-and-when-in-use location permission",
            failures)
    require("NSLocationWhenInUseUsageDescription" in app_plist,
            "Info.plist must document when-in-use location permission",
            failures)
    require("location" in app_plist.get("UIBackgroundModes", []),
            "Info.plist must preserve background location mode for visit monitoring",
            failures)
    require("Route.gpx" in project and "LocationsStorage.swift" in project,
            "Xcode project must keep route fixture and storage source references",
            failures)
    require("requestAlwaysAuthorization()" in app_delegate and "startMonitoringVisits()" in app_delegate,
            "AppDelegate must preserve the visit-monitoring sample flow",
            failures)
    delegate_index = app_delegate.find("locationManager.delegate = self")
    authorization_index = app_delegate.find("locationManager.requestAlwaysAuthorization()")
    monitoring_index = app_delegate.find("locationManager.startMonitoringVisits()")
    require(0 <= delegate_index < authorization_index < monitoring_index,
            "AppDelegate must assign the location manager delegate before authorization and visit monitoring",
            failures)

    require("documentsURL = try? fileManager.url" in storage,
            "LocationsStorage must guard document-directory access",
            failures)
    require("(try? fileManager.contentsOfDirectory" in storage,
            "LocationsStorage must guard directory listing",
            failures)
    require("let data = try? encoder.encode(location)" in storage,
            "LocationsStorage must guard JSON encoding",
            failures)
    require("try data.write(to: fileURL, options: .atomic)" in storage,
            "LocationsStorage must write location files atomically",
            failures)
    require("fileName(for location: Location)" in storage and '.json"' in storage,
            "LocationsStorage must use explicit JSON filenames for new saves",
            failures)
    require("try!" not in storage,
            "LocationsStorage must not force-unwrap file-system or JSON operations",
            failures)
    require("func publishSavedLocation(_ location: Location)" in storage and "Thread.isMainThread" in storage,
            "LocationsStorage must centralize saved-location publishing and check the main thread",
            failures)
    require("DispatchQueue.main.async" in storage and "NotificationCenter.default.post(name: .newLocationSaved" in storage,
            "LocationsStorage must dispatch saved-location notifications to the main queue when needed",
            failures)
    for source_name, source in [
        ("MapViewController", map_controller),
        ("PlacesTableViewController", places_controller),
    ]:
        require("NotificationCenter.default.addObserver" in source and "name: .newLocationSaved" in source,
                f"{source_name} must observe new location saves",
                failures)
        require("deinit" in source and "NotificationCenter.default.removeObserver(self, name: .newLocationSaved, object: nil)" in source,
                f"{source_name} must remove the new-location observer on deinit",
                failures)

    generated_patterns = ("xcuserdata", ".xcuserstate", ".DS_Store")
    offenders = [path for path in tracked if any(pattern in path for pattern in generated_patterns)]
    require(not offenders, "generated user-state files must not be tracked: " + ", ".join(offenders), failures)
    for expected in [".DS_Store", "DerivedData/", "xcuserdata/", "*.xcuserstate", "*.local.xcconfig"]:
        require(expected in gitignore, f".gitignore must contain {expected}", failures)

    for path, content in [("README.md", readme), ("VISION.md", vision), ("SECURITY.md", security)]:
        require("make check" in content and "scripts/check-baseline.py" in content,
                f"{path} must document static verification",
                failures)
        require("local" in content.lower() and "location" in content.lower(),
                f"{path} must document local location privacy posture",
                failures)
        require("notification observer" in content.lower(),
                f"{path} must document notification observer lifecycle handling",
                failures)
        require("main-thread notification" in content.lower(),
                f"{path} must document main-thread notification delivery",
                failures)
        require("location manager delegate setup" in content.lower(),
                f"{path} must document location manager delegate setup order",
                failures)
    require("force-unwrap" in changes and "user-state" in changes and "make check" in changes and "notification observer" in changes.lower() and "main-thread notification" in changes.lower(),
            "CHANGES must record storage hardening, metadata cleanup, notification cleanup, main-thread notification delivery, and verification",
            failures)
    require("location manager delegate setup" in changes.lower(),
            "CHANGES must record location manager delegate setup hardening",
            failures)
    require("status: completed" in plan and "Work Completed" in plan and "Verification" in plan,
            "plan must be completed and describe completed work and verification",
            failures)
    require("status: completed" in notification_plan,
            "notification observer lifecycle plan must be marked completed",
            failures)
    require("status: completed" in main_thread_plan,
            "location notification main-thread plan must be marked completed",
            failures)
    require("status: completed" in delegate_plan,
            "location manager delegate setup plan must be marked completed",
            failures)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("Location manager sample baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
