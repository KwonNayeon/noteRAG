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
    @State var isOpened: Bool = false
    @State var keynum: Int = 0
    
    var body: some View {
        VStack {
            Rectangle()
                .frame(width: 1390, height: 1)
                .padding(.bottom, 24)
                .padding(.top, 94)
            HStack {
                ZStack {
                    Rectangle()
                        .frame(width: 655, height: 740)
                        .foregroundStyle(.white)
                    VStack {
                        HStack {
                            Text("Summary Title")
                                .font(.system(size: 45, weight: .bold))
                            Spacer()
                        }
                        HStack {
                            Text("Subtopics")
                                .font(.system(size: 35))
                            Spacer()
                        }
                        HStack {
                            Rectangle()
                                .frame(width: 438, height: 1)
                            Spacer()
                        }
                        
                        HStack {
                            ForEach(0..<3){ num in
                                ZStack {
                                    RoundedRectangle(cornerRadius: 12)
                                        .frame(width: 132, height: 36)
                                        .foregroundStyle(colorPallete[num])
                                    Text("# \(summary.keywords[num])")
                                }
                                .padding(.trailing, 9)
                            }
                            Spacer()
                        }.padding(.top, 27)
                        
                        Button {
                            isOpened = true
                            keynum = 0
                        }label: {
                            HStack {
                                Image(systemName: "image2")
                                    .frame(width: 34, height: 50)
                                Text(makeAttributedString(number: 0))
                                    .foregroundStyle(.black)
                                Spacer()
                            }
                        }
                        Button {
                            isOpened = true
                            keynum = 1
                        }label: {
                            HStack {
                                Image(systemName: "image")
                                    .frame(width: 34, height: 50)
                                Text(makeAttributedString(number: 1))
                                    .foregroundStyle(.black)
                                Spacer()
                            }
                        }
                        Button {
                            isOpened = true
                            keynum = 2
                        }label: {
                            HStack {
                                Image(systemName: "image2")
                                    .frame(width: 34, height: 50)
                                Text(makeAttributedString(number: 2))
                                    .foregroundStyle(.black)
                                Spacer()
                            }
                        }
                        Spacer()
                    }
                    .padding(34)
                }
                
                ZStack {
                    Rectangle()
                        .frame(width: 540, height: 740)
                        .foregroundStyle(.white)
                    
                    // right side
                    if isOpened {
                        VStack {
                            Text("\"\(summary.highLevel[keynum])\"")
                                .font(.system(size: 40, weight: .bold))
                                .frame(width: 400)
                                .multilineTextAlignment(.center)
                            HStack {
                                Image(systemName: "image2")
                                    .frame(width: 34, height: 50)
                                Text(summary.expanded[3 * keynum])
                                    .foregroundStyle(.black)
                            }
                            HStack {
                                Image(systemName: "image")
                                    .frame(width: 34, height: 50)
                                Text(summary.expanded[3 * keynum + 1])
                                    .foregroundStyle(.black)
                            }
                            HStack {
                                Image(systemName: "image2")
                                    .frame(width: 34, height: 50)
                                Text(summary.expanded[3 * keynum + 2])
                                    .foregroundStyle(.black)
                            }
                            Spacer()
                        }
                        
                    }
                }
            }
        }
    }
    
    func makeAttributedString(number: Int) -> AttributedString {
        let line = summary.highLevel[number]
        let keywords = summary.keywords[number]
        
        guard let randomKeyword = keywords.randomElement().map({ String($0) }),
              line.contains(keywords) else {
            return AttributedString(line)
        }
        
        var attributed = AttributedString(line)
        
        if let range = attributed.range(of: keywords) {
            attributed[range].font = .system(size: 17, weight: .bold)
            attributed[range].backgroundColor = colorPallete[number]
        }
        return attributed
    }
}

#Preview {
    SummaryView(summary: Summary(id: 1, title: "title", subtitle: "subsub", keywords: ["one", "two", "Three"], highLevel: ["Hi my name is one", "two is my second name", "Third Three haha"], expanded: ["III one", "222 two", "33 three", "III one", "222 two", "33 three", "III one", "222 two", "33 three"]))
}
