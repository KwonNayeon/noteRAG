//
//  Sidebar.swift
//  ProjectX-personal
//
//  Created by Choi Minkyeong on 4/12/25.
//

import SwiftUI

struct Sidebar: View {
    let folderName: [String] = ["Bio", "Mathmetics", "Statistics"]
    let summary: [String] = ["Project X", "Schrödinger's cat", "Global warming"]
    
    @State var isExpanded: Bool = false
    
    var body: some View {
        VStack {
            Text("Summary docs")
                .font(.system(size: 29, weight: .bold))
             
            Rectangle()
                .frame(width: 225, height: 1)
                .foregroundStyle(.black)
                .padding(.bottom, 26)
            
            HStack {
                Text("Folders")
                    .font(.system(size: 20))
                    .padding(.bottom, 20)
                Spacer()
            }
            
            ForEach(folderName, id: \.self) { folderName in
                HStack {
                    RoundedRectangle(cornerRadius: 6)
                        .frame(width: 32, height: 25)
                        .foregroundStyle(.orange)
                    
                    Text("\(folderName)")
                        .font(.system(size: 18))
                    
                    Spacer()
                }
            }
            
            HStack {
                Text("Summary")
                    .font(.system(size: 20))
                    .padding(.top, 44)
                    .padding(.bottom, 20)
                Spacer()
            }
            
            ForEach(summary, id: \.self) { summary in
                HStack {
                    Text(" • ")
                        .foregroundStyle(Color(.FF_6_E_00))
                        .padding(.trailing, 15)
                    Text("\(summary)")
                        .font(.system(size: 18))
                    Spacer()
                }
            }
            
            Button {
                isExpanded.toggle()
            } label: {
                HStack{
                    Spacer()
                    Image(systemName: isExpanded ? "arrowtriangle.up.fill": "arrowtriangle.down.fill")
                        .frame(width: 12, height: 11)
                    Text("more")
                        .font(.system(size: 15))
                }
                .foregroundStyle(Color(.AAAAAA))
            }
            
            Spacer()
        }
        .padding(31)
    }
}
