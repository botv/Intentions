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
        let animation = CAKeyframeAnimation(keyPath: "transform.translation.x")
        animation.timingFunction = CAMediaTimingFunction(name: CAMediaTimingFunctionName.linear)
        animation.duration = 0.6
        animation.values = [-20.0, 20.0, -20.0, 20.0, -10.0, 10.0, -5.0, 5.0, 0.0 ]
        layer.add(animation, forKey: "shake")
    }
}
