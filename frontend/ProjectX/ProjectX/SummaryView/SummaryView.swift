//
//  SummaryView.swift
//  ProjectX-personal
//
//  Created by Choi Minkyeong on 4/13/25.
//

import SwiftUI

struct SummaryView: View {
    let summary: Summary
    let colorPallete: [Color] = [Color(.FFCDA_7), Color(.FCE_8_B_0), Color(.CDEFF_8)]
    let imageNames = ["WhitePointer", "BlackPointer", "WhitePointer"]
    @State var isOpened: Bool = false
    @State var keynum: Int = 0
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                Button {
                    
                } label: {
                    ZStack {
                        Circle()
                            .foregroundStyle(Color(.FCE_8_B_0))
                            .frame(width: 50)
                            .padding(.vertical, 24)
                        
                        Image(systemName: "house")
                            .font(.title2)
                    }
                }
                
                Circle()
                    .foregroundStyle(Color(.FFD_666))
                    .frame(width: 50)
                    .padding(.trailing, 22)
                    .padding(.vertical, 24)
            }
            
            Rectangle()
                .frame(width: 1390, height: 1)
                .padding(.bottom, 24)
            HStack {
                ZStack {
                    Rectangle()
                        .frame(width: 655, height: 740)
                        .foregroundStyle(.white)
                    HStack {
                        Spacer()
                        Rectangle()
                            .frame(width: 1, height: 914)
                            .foregroundStyle(.black)
                    }
                    
                    VStack {
                        HStack {
                            Text("\(summary.title)")
                                .font(.system(size: 45, weight: .bold))
                            Spacer()
                        }
                        HStack {
                            Text("\(summary.topic ?? "")")
                                .font(.system(size: 35))
                            Spacer()
                        }
                        HStack {
                            Rectangle()
                                .frame(width: 438, height: 1)
                            Spacer()
                        }
                        
                        HStack {
                            ForEach(0..<min(3, summary.keywords.count), id: \.self){ num in
                                HStack {
                                    Text("# \(summary.keywords[num])")
                                        .font(.system(size: 25))
                                        .foregroundStyle(.black)
                                        .padding(.leading, 15)
                                    Spacer()
                                }
                                .background {
                                    RoundedRectangle(cornerRadius: 12)
                                        .foregroundStyle(colorPallete[num])
                                        
                                }
                                .frame(width: 132, height: 36)
                                .padding(.trailing, 9)
                            }
                            Spacer()
                        }
                        .padding(.top, 27)
                        .padding(.bottom, 38)
                        
                        VStack {
                            ForEach(0..<imageNames.count, id: \.self) { index in
                                Button {
                                    isOpened = true
                                    keynum = index
                                } label: {
                                    HStack {
                                        Image(imageNames[index])
                                            .resizable()
                                            .frame(width: 34, height: 50)
                                        
                                        Text(makeAttributedString(number: index))
                                            .foregroundStyle(.black)
                                            .font(.system(size: 25))
                                            .multilineTextAlignment(.leading)
                                            .lineLimit(nil)
                                            .fixedSize(horizontal: false, vertical: true)

                                        Spacer()
                                    }
                                }
                            }
                        }
                        
                        Image("shu")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 400, height: 400)

                        Spacer()
                    }
                    .padding(34)
                }
                
                ZStack {
                    Rectangle()
                        .frame(width: 540, height: 740)
                        .foregroundStyle(.white)
                    
                    if isOpened {
                        VStack {
                            Text("\"\(summary.lines[keynum])\"")
                                .font(.system(size: 35, weight: .bold))
                                .frame(width: 400)
                                .multilineTextAlignment(.center)
                                .padding(.bottom, 100)
                            
                            VStack {
                                ForEach(0..<3, id: \.self) { i in
                                    HStack {
                                        Image(imageNames[i])
                                            .resizable()
                                            .frame(width: 34, height: 50)
                                        Text(summary.expanded[keynum][i])
                                            .foregroundStyle(.black)
                                            .multilineTextAlignment(.leading)
                                        Spacer()
                                    }
                                }
                            }
                            .padding(.horizontal, 76)
                            
                            Image("learning")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 400, height: 400)
                            
                            Spacer()
                        }
                    }
                }
                .frame(width: 540, height: 740)
            }
        }
    }
    
    func textTrimming(text: String) -> String {
        var text = "\"\"\"Hello, World!\"\"\""
        text = text.trimmingCharacters(in: CharacterSet(charactersIn: "\""))

        if text.count >= 3 {
            text = String(text.dropFirst(3))
        }
        
        return text
    }
    
    func makeAttributedString(number: Int) -> AttributedString {
        guard summary.lines.indices.contains(number),
                  summary.keywords.indices.contains(number) else {
                return AttributedString("")
            }
        
        let line = summary.lines[number]
        let keywords = summary.keywords[number]
        
        guard let randomKeyword = keywords.randomElement().map({ String($0) }),
              line.contains(keywords) else {
            return AttributedString(line)
        }
        
        var attributed = AttributedString(line)
        
        if let range = attributed.range(of: keywords) {
            attributed[range].font = .system(size: 25, weight: .bold)
            attributed[range].backgroundColor = colorPallete[number]
        }
        return attributed
    }
}

#Preview {
    SummaryView(summary: Summary(id: 1, title: "title", topic: "subsub", keywords: ["onㄹㄹㄹㄹㄹㄹㄹㄹe", "tㄹㄹㄹㄹㄹㄹㄹwo", "Thrㄹㄹㄹㄹㄹㄹㄹㄹee"], lines: ["Hi bllblblblbkjflkdjkgjdlfkgjldkfjgldkfdflkgjdlkfgjkfdjglkfdjglkdjflgky name is one", "two is my second name", "Third Three haha"], expanded: [["III one", "222 two", "33 three"], ["III one", "222 two", "33 three"], ["III one", "222 two", "33 three"]]))
}
