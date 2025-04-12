//
//  DetailView.swift
//  ProjectX-personal
//
//  Created by Choi Minkyeong on 4/12/25.
//

import SwiftUI

struct DetailView: View {
    @State private var showingImporter = false
    @State private var pdfData: Data?
    
    // 2. State for the AI response
    @State private var summary: Summary = Summary(id: 0, title: "", subtitle: "", keywords: [], highLevel: [], expanded: [])
    @State private var isLoading = false
    
    @State private var navigateToSummary = false
    
    var body: some View {
        VStack {
            // Welcome User
            HStack {
                Spacer()
                VStack {
                    HStack {
                        Spacer()
                        Text("Welcome,")
                            .bold()
                    }
                    HStack {
                        Spacer()
                        Text("ProjectX")
                    }
                }
                .font(.system(size: 25))
                
                Circle()
                    .foregroundStyle(Color(.FF_6_E_00))
                    .frame(width: 50)
            }
            
            Spacer()
            
            // File Upload
            HStack {
                Text("Wanna")
                    .bold()
                    .foregroundStyle(Color(.F_00_A_7_D_0))
                Text("Summary?")
                    .bold()
                    .foregroundStyle(Color(.F_065_E_74))
            }
            .font(.system(size: 60, weight: .heavy))
            
            Button(action: {
                showingImporter = true
            }) {
                ZStack {
                    RoundedRectangle(cornerRadius: 13)
                        .frame(width: 736, height: 240)
                        .foregroundStyle(Color(.FCE_8_B_0))
                    
                    VStack {
                        Text("Click to")
                            .font(.system(size: 35))
                            .foregroundStyle(Color(.FF_6_E_00))
                            .padding(.top, 55)
                        
                        HStack {
                            Text("Upload")
                                .font(.system(size: 50, weight: .heavy))
                            Text(" Your File")
                        }
                        .font(.system(size: 50))
                        .foregroundStyle(Color(.FF_6_E_00))
                    }
                    .padding(.bottom, 55)
                    
                }
            }
            .fileImporter(
                isPresented: $showingImporter,
                allowedContentTypes: [.pdf]
            ) { result in
                switch result {
                case .success(let url):
                    Task {
                        pdfData = try? Data(contentsOf: url)
                        await uploadPDF()
                    }
                case .failure(let err):
                    print("Import failed:", err)
                }
            }
            // 4. Show loading / result
            if isLoading {
                ProgressView("Summarizing…")
            } else if !summary.title.isEmpty {
                Text(summary.title)
                    .padding()
                    .border(Color.gray)
            }
            
            NavigationLink(
                destination: SummaryView(summary: summary),
                isActive: $navigateToSummary
            ) {
                EmptyView()
            }
            
            Spacer()
        }
        
    }
    
    // 5. The uploadPDF function you already have
    func uploadPDF() async {
        guard let pdfData = pdfData else { return }
        isLoading = true
        defer { isLoading = false }
        
        guard let url = URL(string: "http://<YOUR-SERVER>/api/simplify_pdf") else {
            print("❌ Wrong URL")
            return
        }

        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        req.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        // Build the multipart body
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"doc.pdf\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/pdf\r\n\r\n".data(using: .utf8)!)
        body.append(pdfData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        do {
            let (data, _) = try await URLSession.shared.upload(for: req, from: body)
            // Decode your JSON response however you defined it:
            let resp = try JSONDecoder().decode(ResponsePayload.self, from: data)
            // For simplicity, assume it has a single summary string:
            summary.title = resp.summaries.first?.highLevel.joined(separator: "\n") ?? ""
            navigateToSummary = true
        } catch {
            summary.title = "Error: \(error.localizedDescription)"
        }
    }
}

// 6. Your Codable response models
struct Summary: Identifiable, Codable {
    var id: Int
    var title: String
    var subtitle: String
    var keywords: [String]
    var highLevel: [String]
    var expanded: [String]
}

struct ResponsePayload: Codable {
    let summaries: [Summary]
}
