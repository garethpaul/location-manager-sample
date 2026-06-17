#!/usr/bin/env python3
from pathlib import Path
import json
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-location-storage-baseline.md"
LATEST_LOCATION_PLAN = ROOT / "docs/plans/2026-06-09-latest-location-update-selection.md"
CHECKOUT_CREDENTIAL_PLAN = ROOT / "docs/plans/2026-06-12-checkout-credential-boundary.md"
CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_MAKEFILE = """ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: build check lint test

lint test build: check

check:
\tpython3 "$(ROOT)/scripts/check-baseline.py"
"""


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


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
        ".github/workflows/check.yml",
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
        "docs/plans/2026-06-09-places-table-index-guard.md",
        "docs/plans/2026-06-09-location-json-file-filter.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-09-redacted-location-notification.md",
        "docs/plans/2026-06-09-latest-location-update-selection.md",
        "docs/plans/2026-06-10-reverse-geocode-fallback-description.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-bounded-location-loads.md",
        "docs/plans/2026-06-12-checkout-credential-boundary.md",
        "docs/plans/2026-06-13-unique-location-filenames.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-14-chronological-location-publishing.md",
        "docs/plans/2026-06-14-save-coordinate-validation.md",
        "docs/plans/2026-06-15-bounded-location-count-integration.md",
        "docs/plans/2026-06-16-retained-location-file-cap.md",
        "docs/plans/2026-06-17-retained-location-file-eligibility.md",
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
    makefile = read("Makefile")
    gitignore = read(".gitignore")
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    delegate_plan_path = ROOT / "docs/plans/2026-06-08-location-manager-delegate-setup.md"
    delegate_plan = delegate_plan_path.read_text(encoding="utf-8") if delegate_plan_path.exists() else ""
    main_thread_plan = read("docs/plans/2026-06-08-location-notification-main-thread.md")
    notification_plan = read("docs/plans/2026-06-08-notification-observer-lifecycle.md")
    table_index_plan = read("docs/plans/2026-06-09-places-table-index-guard.md")
    json_filter_plan = read("docs/plans/2026-06-09-location-json-file-filter.md")
    make_gates_plan = read("docs/plans/2026-06-09-make-gate-aliases.md")
    redacted_notification_plan = read("docs/plans/2026-06-09-redacted-location-notification.md")
    latest_location_plan = LATEST_LOCATION_PLAN.read_text(encoding="utf-8") if LATEST_LOCATION_PLAN.exists() else ""
    reverse_geocode_plan = read("docs/plans/2026-06-10-reverse-geocode-fallback-description.md")
    hosted_validation_plan = read("docs/plans/2026-06-10-hosted-project-validation.md")
    bounded_loads_plan = read("docs/plans/2026-06-10-bounded-location-loads.md")
    checkout_credential_plan = (
        CHECKOUT_CREDENTIAL_PLAN.read_text(encoding="utf-8")
        if CHECKOUT_CREDENTIAL_PLAN.exists()
        else ""
    )
    unique_filenames_plan = read("docs/plans/2026-06-13-unique-location-filenames.md")
    location_independent_make_plan = read("docs/plans/2026-06-13-location-independent-make.md")
    chronological_publish_plan = read("docs/plans/2026-06-14-chronological-location-publishing.md")
    save_coordinate_plan = read("docs/plans/2026-06-14-save-coordinate-validation.md")
    bounded_count_plan = read("docs/plans/2026-06-15-bounded-location-count-integration.md")
    retained_file_cap_plan = read("docs/plans/2026-06-16-retained-location-file-cap.md")
    retained_file_eligibility_plan = read("docs/plans/2026-06-17-retained-location-file-eligibility.md")
    workflow = read(".github/workflows/check.yml")
    workflow_files = [
        *sorted((ROOT / ".github/workflows").glob("*.yml")),
        *sorted((ROOT / ".github/workflows").glob("*.yaml")),
    ]
    tracked = git_ls_files()

    require(makefile == EXPECTED_MAKEFILE,
            "Makefile must exactly preserve rooted lint, test, build, and check gates",
            failures)
    require("make -f /path/to/location-manager-sample/Makefile check" in readme,
            "README must document location-independent Makefile invocation",
            failures)

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
    require('content.body = "A new location was saved."' in app_delegate and
            "content.body = location.description" not in app_delegate,
            "local visit notifications must use a redacted body instead of precise location details",
            failures)
    require("guard let location = locations.last else" in app_delegate and "locations.first" not in app_delegate,
            "location update simulation must use the latest batched CoreLocation update",
            failures)
    require(app_delegate.count('?? "Saved location"') >= 2 and
            'let description = "Fake visit: \\(placeDescription)"' in app_delegate,
            "AppDelegate must save visits with fallback descriptions when reverse geocoding has no placemark",
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
    filename_helper = storage[
        storage.find("private func fileName(for location: Location)"):
        storage.find("}\n}", storage.find("private func fileName(for location: Location)"))
    ]
    require(filename_helper.count("location.date.timeIntervalSince1970") == 1 and
            filename_helper.count("UUID().uuidString") == 1 and
            filename_helper.count('.json"') == 1 and
            'return "\\(location.date.timeIntervalSince1970).json"' not in filename_helper,
            "LocationsStorage must give every new JSON location file a unique timestamp-prefixed name",
            failures)
    require('url.pathExtension.lowercased() == "json"' in storage,
            "LocationsStorage must filter persisted location loads to JSON files",
            failures)
    resource_values_index = storage.find("url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey])")
    data_read_index = storage.find("Data(contentsOf: candidate.url)")
    require("maximumLocationFileSize = 64 * 1024" in storage and
            resource_values_index >= 0 and
            "resourceValues.isRegularFile == true" in storage and
            "fileSize <= LocationsStorage.maximumLocationFileSize" in storage and
            data_read_index > resource_values_index,
            "LocationsStorage must reject non-regular or oversized JSON files before reading them",
            failures)
    timestamp_helper_start = storage.find("private static func timestamp(fromLocationFileURL url: URL)")
    timestamp_helper_end = storage.find("\n  func saveLocationOnDisk", timestamp_helper_start)
    timestamp_helper = storage[timestamp_helper_start:timestamp_helper_end]
    candidate_start = storage.find("let locationFileCandidates = locationFilesURLs.compactMap")
    newest_first = storage.find("}.sorted(by: {", candidate_start)
    count_prefix = storage.find(".prefix(LocationsStorage.maximumLocationFileCount)", newest_first)
    chronological_sort = storage.find(".sorted(by: { $0.date < $1.date })", data_read_index)
    require("maximumLocationFileCount = 1000" in storage and
            timestamp_helper_start >= 0 and timestamp_helper_end >= 0 and
            "TimeInterval(fileName)" in timestamp_helper and
            'fileName.dropFirst().firstIndex(of: "-")' in timestamp_helper and
            "UUID(uuidString:" in timestamp_helper and
            timestamp_helper.count("timestamp.isFinite") == 2 and
            "if $0.timestamp == $1.timestamp" in storage and
            "return $0.url.lastPathComponent > $1.url.lastPathComponent" in storage and
            "return $0.timestamp > $1.timestamp" in storage and
            -1 not in (candidate_start, newest_first, count_prefix, data_read_index,
                       chronological_sort) and
            candidate_start < newest_first < count_prefix < data_read_index < chronological_sort,
            "LocationsStorage must parse legacy and unique timestamp names and bound newest candidates before reading data",
            failures)
    require("CLLocationCoordinate2DIsValid(location.coordinates)" in storage,
            "LocationsStorage must reject persisted locations with invalid coordinates",
            failures)
    save_start = storage.find("func saveLocationOnDisk(_ location: Location)")
    save_end = storage.find("\n  private func publishSavedLocation", save_start)
    save_helper = storage[save_start:save_end]
    save_coordinate_guard_index = save_helper.find(
        "guard CLLocationCoordinate2DIsValid(location.coordinates) else"
    )
    encoder_index = save_helper.find("let encoder = JSONEncoder()")
    file_url_index = save_helper.find("let fileURL = documentsURL.appendingPathComponent")
    write_index = save_helper.find("try data.write(to: fileURL, options: .atomic)")
    prune_index = save_helper.find("prunePersistedLocationFiles(in: documentsURL)")
    publish_index = save_helper.find("publishSavedLocation(location)")
    require(save_start >= 0 and
            save_end > save_start and
            save_coordinate_guard_index >= 0 and
            encoder_index > save_coordinate_guard_index and
            file_url_index > save_coordinate_guard_index and
            write_index > save_coordinate_guard_index and
            prune_index > write_index and
            publish_index > save_coordinate_guard_index and
            publish_index > prune_index and
            save_helper.count("CLLocationCoordinate2DIsValid(location.coordinates)") == 1,
            "LocationsStorage must reject invalid coordinates before save side effects",
            failures)
    prune_start = storage.find("private func prunePersistedLocationFiles(in documentsURL: URL)")
    prune_end = storage.find("\n  private func publishSavedLocation", prune_start)
    prune_helper = storage[prune_start:prune_end]
    prune_sort_index = prune_helper.find("}.sorted(by: {")
    prune_drop_index = prune_helper.find(
        "candidates.dropFirst(LocationsStorage.maximumLocationFileCount)"
    )
    prune_remove_index = prune_helper.find("try? fileManager.removeItem(at: candidate.url)")
    require(prune_start >= 0 and prune_end > prune_start and
            "try? fileManager.contentsOfDirectory" in prune_helper and
            'url.pathExtension.lowercased() == "json"' in prune_helper and
            "includingPropertiesForKeys: [.isRegularFileKey, .fileSizeKey]" in prune_helper and
            "url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey])" in prune_helper and
            "resourceValues.isRegularFile == true" in prune_helper and
            "let fileSize = resourceValues.fileSize" in prune_helper and
            "fileSize <= LocationsStorage.maximumLocationFileSize" in prune_helper and
            "LocationsStorage.timestamp(fromLocationFileURL: url)" in prune_helper and
            "if $0.timestamp == $1.timestamp" in prune_helper and
            "return $0.url.lastPathComponent > $1.url.lastPathComponent" in prune_helper and
            "return $0.timestamp > $1.timestamp" in prune_helper and
            -1 not in (prune_sort_index, prune_drop_index, prune_remove_index) and
            prune_sort_index < prune_drop_index < prune_remove_index and
            storage.count("fileManager.removeItem(at:") == 1,
            "LocationsStorage must prune only oldest size-eligible compatible regular location JSON files after a successful write",
            failures)
    require("try!" not in storage,
            "LocationsStorage must not force-unwrap file-system or JSON operations",
            failures)
    require("func publishSavedLocation(_ location: Location)" in storage and "Thread.isMainThread" in storage,
            "LocationsStorage must centralize saved-location publishing and check the main thread",
            failures)
    publish_start = storage.find("private func publishSavedLocation(_ location: Location)")
    publish_end = storage.find("\n  func saveCLLocationToDisk", publish_start)
    publish_helper = storage[publish_start:publish_end]
    insertion_index = publish_helper.find("self.locations.firstIndex { $0.date > location.date }")
    insert_index = publish_helper.find("self.locations.insert(location, at: insertionIndex)")
    notification_index = publish_helper.find("NotificationCenter.default.post(name: .newLocationSaved")
    require(insertion_index >= 0 and
            "?? self.locations.endIndex" in publish_helper and
            insert_index > insertion_index and
            notification_index > insert_index and
            "self.locations.append(location)" not in publish_helper,
            "LocationsStorage must insert successful saves chronologically before publishing notifications",
            failures)
    require("DispatchQueue.main.async" in storage and "NotificationCenter.default.post(name: .newLocationSaved" in storage,
            "LocationsStorage must dispatch saved-location notifications to the main queue when needed",
            failures)
    require('?? "Saved location"' in storage and "self.saveLocationOnDisk(location)" in storage,
            "LocationsStorage must save map-added locations with fallback descriptions when reverse geocoding has no placemark",
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
    require("let locations = LocationsStorage.shared.locations" in places_controller and
            "guard indexPath.row < locations.count" in places_controller and
            "let location = locations[indexPath.row]" in places_controller,
            "PlacesTableViewController must guard row indexes before reading saved locations",
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
        require("table index guard" in content.lower(),
                f"{path} must document places table index guard handling",
                failures)
        require("JSON file filter" in content,
                f"{path} must document saved-location JSON file filter handling",
                failures)
        require("redacted notification body" in content.lower(),
                f"{path} must document redacted location notification bodies",
                failures)
        require("latest location update" in content.lower(),
                f"{path} must document latest location update selection",
                failures)
        require("reverse-geocode fallback" in content.lower(),
                f"{path} must document reverse-geocode fallback descriptions",
                failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme,
            "README must document the standard local verification gates",
            failures)
    require("make lint" in vision and "make test" in vision and "make build" in vision,
            "VISION must document the standard local verification gates",
            failures)
    require("make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record the standard local verification gates",
            failures)
    require("force-unwrap" in changes and "user-state" in changes and "make check" in changes and "notification observer" in changes.lower() and "main-thread notification" in changes.lower() and "JSON file filter" in changes and "redacted notification body" in changes.lower(),
            "CHANGES must record storage hardening, metadata cleanup, notification cleanup, main-thread notification delivery, JSON file filtering, redacted notification bodies, and verification",
            failures)
    require("latest location update" in changes.lower(),
            "CHANGES must record latest location update selection",
            failures)
    require("reverse-geocode fallback" in changes.lower(),
            "CHANGES must record reverse-geocode fallback descriptions",
            failures)
    require("location manager delegate setup" in changes.lower(),
            "CHANGES must record location manager delegate setup hardening",
            failures)
    require("table index guard" in changes.lower(),
            "CHANGES must record places table index guard hardening",
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
    require("status: completed" in table_index_plan,
            "places table index guard plan must be marked completed",
            failures)
    require("status: completed" in json_filter_plan,
            "saved-location JSON file filter plan must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in redacted_notification_plan,
            "redacted location notification plan must be marked completed",
            failures)
    require("status: completed" in latest_location_plan,
            "latest location update selection plan must be marked completed",
            failures)
    require("status: completed" in reverse_geocode_plan,
            "reverse-geocode fallback plan must be marked completed",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be marked completed",
            failures)
    unique_filenames_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", unique_filenames_plan)
    unique_filenames_verification = markdown_section(
        unique_filenames_plan, "Verification Completed"
    )
    unique_filenames_evidence = [
        "all four Make gates passed",
        "four hostile mutations were rejected",
        "xcodebuild was unavailable",
        "No simulator, device, Core Location, or live filesystem runtime verification is claimed",
    ]
    require(unique_filenames_status == ["completed"] and
            unique_filenames_verification and
            all(evidence in unique_filenames_verification for evidence in unique_filenames_evidence) and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", unique_filenames_verification),
            "unique location filenames plan must record completed status and actual verification",
            failures)
    require("status: completed" in location_independent_make_plan and
            "root and external-directory" in location_independent_make_plan and
            "five isolated hostile mutations" in location_independent_make_plan,
            "location-independent Make plan must record completed root, external, and mutation verification",
            failures)
    chronological_publish_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", chronological_publish_plan
    )
    chronological_publish_verification = markdown_section(
        chronological_publish_plan, "Verification Completed"
    )
    require(chronological_publish_status == ["completed"] and
            chronological_publish_verification and
            "All four Make gates passed" in chronological_publish_verification and
            "external directory" in chronological_publish_verification and
            "Six isolated hostile mutations were rejected" in chronological_publish_verification and
            "`xcodebuild` is unavailable" in chronological_publish_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", chronological_publish_verification),
            "chronological location publishing plan must record completed status and actual verification",
            failures)
    save_coordinate_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", save_coordinate_plan
    )
    save_coordinate_verification = markdown_section(
        save_coordinate_plan, "Verification Completed"
    )
    require(save_coordinate_status == ["completed"] and
            save_coordinate_verification and
            "All four Make gates passed" in save_coordinate_verification and
            "external directory" in save_coordinate_verification and
            "Six isolated hostile mutations were rejected" in save_coordinate_verification and
            "`xcodebuild` is unavailable" in save_coordinate_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", save_coordinate_verification),
            "save coordinate validation plan must record completed status and actual verification",
            failures)
    bounded_count_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", bounded_count_plan)
    bounded_count_verification = markdown_section(
        bounded_count_plan, "Verification Completed"
    )
    require(bounded_count_status == ["completed"] and
            bounded_count_verification and
            "All four Make gates passed" in bounded_count_verification and
            "external-directory Make gate" in bounded_count_verification and
            "Nine isolated hostile mutations were rejected" in bounded_count_verification and
            "git diff --check" in bounded_count_verification and
            "xcodebuild is unavailable" in bounded_count_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", bounded_count_verification),
            "bounded location count integration plan must record completed status and actual verification",
            failures)
    retained_file_cap_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", retained_file_cap_plan
    )
    retained_file_cap_verification = markdown_section(
        retained_file_cap_plan, "Verification Completed"
    )
    require(retained_file_cap_status == ["completed"] and
            retained_file_cap_verification and
            "All four Make gates passed" in retained_file_cap_verification and
            "external-directory Make gate" in retained_file_cap_verification and
            "Seven isolated hostile mutations were rejected" in retained_file_cap_verification and
            "git diff --check" in retained_file_cap_verification and
            "xcodebuild is unavailable" in retained_file_cap_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", retained_file_cap_verification),
            "retained location file cap plan must record completed status and actual verification",
            failures)
    retained_file_eligibility_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", retained_file_eligibility_plan
    )
    retained_file_eligibility_verification = markdown_section(
        retained_file_eligibility_plan, "Verification Completed"
    )
    require(retained_file_eligibility_status == ["completed"] and
            retained_file_eligibility_verification and
            "All four Make gates passed" in retained_file_eligibility_verification and
            "absolute Makefile gate passed" in retained_file_eligibility_verification and
            "Five isolated hostile mutations were rejected" in retained_file_eligibility_verification and
            "exact diff" in retained_file_eligibility_verification and
            "xcodebuild` is unavailable" in retained_file_eligibility_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", retained_file_eligibility_verification),
            "retained location file eligibility plan must record completed status and actual verification",
            failures)
    bounded_loads_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", bounded_loads_plan)
    bounded_loads_work = markdown_section(bounded_loads_plan, "Work Completed")
    bounded_loads_verification = markdown_section(
        bounded_loads_plan, "Verification Completed"
    )
    require(bounded_loads_status == ["completed"] and bounded_loads_work,
            "bounded location loads plan must record one completed status and completed work",
            failures)
    require(bounded_loads_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", bounded_loads_verification),
            "bounded location loads plan must record finished verification without pending markers",
            failures)
    for evidence in [
        "make check",
        "make lint",
        "make test",
        "make build",
        "python3 -m py_compile scripts/check-baseline.py",
        "git diff --check",
        "27287434242",
        "27402324815",
        "6f9a8f1ec70fab6c08b5920c4cd3544dd0a59760",
        "resourceValues.isRegularFile == true",
        "fileSize <= LocationsStorage.maximumLocationFileSize",
        "CLLocationCoordinate2DIsValid(location.coordinates)",
    ]:
        require(evidence in bounded_loads_verification,
                f"bounded location loads plan must preserve verification evidence: {evidence}",
                failures)
    require("permissions:\n  contents: read" in workflow and "cancel-in-progress: true" in workflow and
            "runs-on: macos-15" in workflow and "timeout-minutes: 10" in workflow and
            CHECKOUT_ACTION in workflow and
            "run: make check" in workflow,
            "Check workflow must stay pinned, read-only, and bounded",
            failures)
    require("New location writes use timestamp-prefixed unique JSON filenames" in readme and
            "New location writes should use timestamp-prefixed unique JSON filenames" in security and
            "New location writes use timestamp-prefixed unique JSON filenames" in vision and
            "Added timestamp-prefixed unique JSON filenames for new location writes" in changes,
            "Project guidance must document unique persisted location filenames",
            failures)
    require("Successful saves are inserted by date before observers are notified" in readme and
            "Successful saves should be inserted chronologically before views are notified" in security and
            "Keep successful in-memory saves ordered by date before notifying views" in vision and
            "Kept successful in-memory location saves ordered by date before notifying" in changes,
            "Project guidance must document chronological in-memory location publishing",
            failures)
    require("Successful saves best-effort prune compatible location JSON files toward the newest 1,000" in " ".join(readme.split()) and
            "Successful saves should best-effort prune compatible location JSON files toward the newest 1,000" in " ".join(security.split()) and
            "Best-effort prune successful saves toward the 1,000 newest compatible location JSON files" in " ".join(vision.split()) and
            "Added best-effort successful-save pruning toward the 1,000 newest compatible location JSON files" in " ".join(changes.split()),
            "Project guidance must document bounded compatible location-file retention",
            failures)
    require("same 64 KiB size eligibility as startup reads" in " ".join(readme.split()) and
            "same 64 KiB size eligibility as startup reads" in " ".join(security.split()) and
            "oversized files outside the size-eligible retention budget" in " ".join(vision.split()) and
            "oversized location-shaped JSON files do not displace valid retained entries" in " ".join(changes.split()),
            "Project guidance must align retained location pruning with startup size eligibility",
            failures)
    require("New location saves reject invalid coordinates before file creation or publication" in readme and
            "New location saves should reject invalid coordinates before file creation or publication" in security and
            "Reject invalid new location saves before file creation or publication" in vision and
            "Rejected invalid new location coordinates before file creation or publication" in changes,
            "Project guidance must document save-time coordinate validation",
            failures)
    require("Startup reads at most 1,000 newest eligible location JSON files" in readme and
            "Startup should read at most 1,000 newest eligible location JSON files" in security and
            "Keep startup reads bounded to the 1,000 newest eligible location JSON files" in vision and
            "Bounded startup reads to the 1,000 newest eligible location JSON files" in changes,
            "Project guidance must document the compatible persisted location count boundary",
            failures)
    checkout_blocks = re.findall(
        rf"(?m)^(?P<indent> *)- +uses: +{re.escape(CHECKOUT_ACTION)}[^\n]*\n"
        rf"(?P=indent)  with:\n"
        rf"(?P=indent)    persist-credentials: +false *$",
        workflow,
    )
    checkout_actions = re.findall(
        r"(?m)^\s*-\s+uses:\s+actions/checkout@",
        workflow,
    )
    require(len(workflow_files) == 1 and
            workflow.count("permissions:") == 1 and
            workflow.count("contents: read") == 1 and
            not re.search(r"(?m)^\s*[A-Za-z-]+:\s*write\s*$", workflow) and
            len(checkout_actions) == 1 and
            workflow.count(CHECKOUT_ACTION) == 1 and
            len(checkout_blocks) == 1 and
            workflow.count("persist-credentials: false") == 1 and
            "persist-credentials: true" not in workflow,
            "Check workflow must keep one read-only permission block and one pinned, credential-free checkout",
            failures)
    checkout_plan_status = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$",
        checkout_credential_plan,
    )
    checkout_plan_work = markdown_section(
        checkout_credential_plan,
        "Work Completed",
    )
    checkout_plan_verification = markdown_section(
        checkout_credential_plan,
        "Verification Completed",
    )
    require(checkout_plan_status == ["completed"] and
            checkout_plan_work and
            "make check" in checkout_plan_verification,
            "checkout credential boundary plan must record one completed status, completed work, and make check verification",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            ["xcodebuild", "-list", "-project", "Journal.xcodeproj"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        require(result.returncode == 0,
                "xcodebuild could not parse Journal.xcodeproj: " + result.stderr.strip(), failures)
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("Location manager sample baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
