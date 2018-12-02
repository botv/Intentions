//
//  MessagesViewController.swift
//  Intentions MessagesExtension
//
//  Created by Ben Botvinick on 12/1/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import UIKit
import Messages

class MessagesViewController: MSMessagesAppViewController {
    
    @IBOutlet weak var keyboardHeightLayoutConstraint: NSLayoutConstraint!
    @IBOutlet weak var messageTextField: UITextField! {
        didSet {
            // Round corners.
            messageTextField.layer.cornerRadius = 20.0
            messageTextField.layer.masksToBounds = true
            messageTextField.layer.borderWidth = 0.5
            messageTextField.layer.borderColor = UIColor.lightGray.cgColor
            
            // Set left padding.
            messageTextField.leftView = UIView(frame: CGRect(x: 0.0, y: 0.0, width: 5.0, height: 2.0))
            messageTextField.leftViewMode = .always
            
            // Set right padding.
            messageTextField.rightView = UIView(frame: CGRect(x: 0.0, y: 0.0, width: 40.0, height: 2.0))
            messageTextField.rightViewMode = .always
            
        }
    }
    
    var savedConversation: MSConversation?
    var message = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Hide the keyboard when it is tapped around.
        self.hideKeyboardWhenTappedAround()
        
        // Set notification for keyboard movement.
        NotificationCenter.default.addObserver(self,  selector: #selector(self.keyboardNotification(notification:)), name: UIResponder.keyboardWillChangeFrameNotification, object: nil)
    }
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }
    
    @objc func keyboardNotification(notification: NSNotification) {
        if let userInfo = notification.userInfo {
            let endFrame = (userInfo[UIResponder.keyboardFrameEndUserInfoKey] as? NSValue)?.cgRectValue
            let endFrameY = endFrame!.origin.y
            let duration: TimeInterval = (userInfo[UIResponder.keyboardAnimationDurationUserInfoKey] as? NSNumber)?.doubleValue ?? 0
            let animationCurveRawNSN = userInfo[UIResponder.keyboardAnimationCurveUserInfoKey] as? NSNumber
            let animationCurveRaw = animationCurveRawNSN?.uintValue ?? UIView.AnimationOptions.curveEaseInOut.rawValue
            let animationCurve: UIView.AnimationOptions = UIView.AnimationOptions(rawValue: animationCurveRaw)
            if endFrameY >= UIScreen.main.bounds.size.height {
                self.keyboardHeightLayoutConstraint?.constant = 0.0
            } else {
                self.keyboardHeightLayoutConstraint?.constant = 0 - (endFrame?.size.height ?? 0.0)
            }
            UIView.animate(withDuration: duration, delay: TimeInterval(0),  options: animationCurve, animations: { self.view.layoutIfNeeded() }, completion: nil)
        }
    }
    
    @IBAction func sendButtonTapped(_ sender: Any) {
        savedConversation?.sendText(message, completionHandler: nil)
    }
    
}
