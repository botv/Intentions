//
//  UIButton+Wiggle.swift
//  Intentions MessagesExtension
//
//  Created by Ben Botvinick on 12/2/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import Foundation
import UIKit

extension UIButton {
    func wiggle() {
        let wiggleAnim = CABasicAnimation(keyPath: "position")
        wiggleAnim.duration = 0.1
        wiggleAnim.repeatCount = 2
        wiggleAnim.autoreverses = true
        wiggleAnim.fromValue = CGPoint(x: self.center.x - 4.0, y: self.center.y)
        wiggleAnim.toValue = CGPoint(x: self.center.x + 4.0, y: self.center.y)
        layer.add(wiggleAnim, forKey: "position")
    }
}
