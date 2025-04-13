//
//  ParsingManager.swift
//  ProjectX
//
//  Created by Choi Minkyeong on 4/13/25.
//

import SwiftUI

// 6. Your Codable response models
struct Summary: Identifiable, Codable {
    var id: Int
    var title: String
    var topic: String?
    var keywords: [String]
    var lines: [String]
    var expanded: [[String]]
}

struct ResponsePayload: Codable {
    let summaries: [Summary]
}

class ParsingManager: ObservableObject {
    @Published var summary: Summary = Summary(id: 0, title: "", topic: "", keywords: [], lines: [], expanded: [[]])
    
    func parseSummaryData(from jsonData: Data) -> Summary? {
        let decoder = JSONDecoder()
        do {
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print("JSON Response: \(jsonString)")
            }
            let response = try decoder.decode(ResponsePayload.self, from: jsonData)
            return response.summaries.first
        } catch {
            print("Decoding failed: \(error)")
            return nil
        }
    }


}

