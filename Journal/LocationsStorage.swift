/// Copyright (c) 2018 Razeware LLC
/// 
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
/// 
/// The above copyright notice and this permission notice shall be included in
/// all copies or substantial portions of the Software.
/// 
/// Notwithstanding the foregoing, you may not use, copy, modify, merge, publish,
/// distribute, sublicense, create a derivative work, and/or sell copies of the
/// Software in any work that is designed, intended, or marketed for pedagogical or
/// instructional purposes related to programming, coding, application development,
/// or information technology.  Permission for such use, copying, modification,
/// merger, publication, distribution, sublicensing, creation of derivative works,
/// or sale is expressly withheld.
/// 
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
/// THE SOFTWARE.

import Foundation
import CoreLocation

class LocationsStorage {
  static let shared = LocationsStorage()
  private static let maximumLocationFileSize = 64 * 1024
  private static let maximumLocationFileCount = 1000
  
  private(set) var locations: [Location]
  private let fileManager: FileManager
  private let documentsURL: URL?
  
  init(fileManager: FileManager = .default) {
    self.fileManager = fileManager
    documentsURL = try? fileManager.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: false)
    
    guard let documentsURL = documentsURL else {
      locations = []
      return
    }
    
    let jsonDecoder = JSONDecoder()
    let locationFilesURLs = (try? fileManager.contentsOfDirectory(at: documentsURL,
                                                                  includingPropertiesForKeys: nil)) ?? []
    let locationFileCandidates = locationFilesURLs.compactMap { url -> (url: URL, timestamp: TimeInterval)? in
      guard url.pathExtension.lowercased() == "json" else {
        return nil
      }
      guard url.lastPathComponent != ".DS_Store" else {
        return nil
      }
      guard let resourceValues = try? url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey]),
            resourceValues.isRegularFile == true,
            let fileSize = resourceValues.fileSize,
            fileSize <= LocationsStorage.maximumLocationFileSize else {
        return nil
      }
      guard let timestamp = LocationsStorage.timestamp(fromLocationFileURL: url) else {
        return nil
      }
      return (url, timestamp)
    }.sorted(by: {
      if $0.timestamp == $1.timestamp {
        return $0.url.lastPathComponent > $1.url.lastPathComponent
      }
      return $0.timestamp > $1.timestamp
    })
      .prefix(LocationsStorage.maximumLocationFileCount)

    locations = locationFileCandidates.compactMap { candidate -> Location? in
      guard let data = try? Data(contentsOf: candidate.url) else {
        return nil
      }
      guard let location = try? jsonDecoder.decode(Location.self, from: data),
            CLLocationCoordinate2DIsValid(location.coordinates) else {
        return nil
      }
      return location
    }.sorted(by: { $0.date < $1.date })
  }

  private static func timestamp(fromLocationFileURL url: URL) -> TimeInterval? {
    let fileName = url.deletingPathExtension().lastPathComponent
    if let timestamp = TimeInterval(fileName), timestamp.isFinite {
      return timestamp
    }

    guard let separatorIndex = fileName.dropFirst().firstIndex(of: "-"),
          let timestamp = TimeInterval(String(fileName[..<separatorIndex])),
          timestamp.isFinite,
          UUID(uuidString: String(fileName[fileName.index(after: separatorIndex)...])) != nil else {
      return nil
    }
    return timestamp
  }
  
  func saveLocationOnDisk(_ location: Location) {
    guard CLLocationCoordinate2DIsValid(location.coordinates) else {
      return
    }

    let encoder = JSONEncoder()
    guard
      let documentsURL = documentsURL,
      let data = try? encoder.encode(location)
    else {
      return
    }

    let fileURL = documentsURL.appendingPathComponent(fileName(for: location))

    do {
      try data.write(to: fileURL, options: .atomic)
    } catch {
      return
    }

    publishSavedLocation(location)
  }

  private func publishSavedLocation(_ location: Location) {
    let publish = {
      let insertionIndex = self.locations.firstIndex { $0.date > location.date } ?? self.locations.endIndex
      self.locations.insert(location, at: insertionIndex)
      NotificationCenter.default.post(name: .newLocationSaved, object: self, userInfo: ["location": location])
    }

    if Thread.isMainThread {
      publish()
    } else {
      DispatchQueue.main.async(execute: publish)
    }
  }

  func saveCLLocationToDisk(_ clLocation: CLLocation) {
    let currentDate = Date()
    AppDelegate.geoCoder.reverseGeocodeLocation(clLocation) { placemarks, _ in
      let description = placemarks?.first.map { "\($0)" } ?? "Saved location"
      let location = Location(clLocation.coordinate, date: currentDate, descriptionString: description)
      self.saveLocationOnDisk(location)
    }
  }

  private func fileName(for location: Location) -> String {
    return "\(location.date.timeIntervalSince1970)-\(UUID().uuidString).json"
  }
}

extension Notification.Name {
  static let newLocationSaved = Notification.Name("newLocationSaved")
}
