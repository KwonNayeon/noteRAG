//
//  ContentView.swift
//  ProjectX-personal
//
//  Created by Choi Minkyeong on 4/12/25.
//

import SwiftUI

struct MainView: View {
    var body: some View {
        NavigationSplitView {
                    Sidebar()
                .background(Color(.FFF_7_E_2))
                } detail: {
                    DetailView()
                        .padding(40)
                }
    }
}

#Preview {
    MainView()
}
