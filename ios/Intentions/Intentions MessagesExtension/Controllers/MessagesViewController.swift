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
    @IBOutlet weak var messageViewHeightLayoutConstraint: NSLayoutConstraint!
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var messageTextView: UITextView! {
        didSet {
            // Round corners.
            messageTextView.layer.cornerRadius = 20.0
            messageTextView.layer.masksToBounds = true
            messageTextView.layer.borderWidth = 0.5
            messageTextView.layer.borderColor = UIColor.lightGray.cgColor
            
            // Set up padding.
            messageTextView.textContainerInset = UIEdgeInsets(top: 8, left: 10.0, bottom: 8, right: 40.0);
            
            // Add placeholder.
            messageTextView.text = messagePlaceholder
            messageTextView.textColor = UIColor.lightGray
            messageTextView.selectedTextRange = messageTextView.textRange(from: messageTextView.beginningOfDocument, to: messageTextView.beginningOfDocument)
        }
    }
    
    var savedConversation: MSConversation?
    var messagePlaceholder = "iMessage"
    var letterCounter = 0
    let frequency = 8
    
    override func viewDidLoad() {
        super.viewDidLoad()
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
                self.keyboardHeightLayoutConstraint?.constant = -(endFrame?.size.height ?? 0.0)
            }
            UIView.animate(withDuration: duration, delay: TimeInterval(0),  options: animationCurve, animations: { self.view.layoutIfNeeded() }, completion: nil)
        }
    }
    
    override func willBecomeActive(with conversation: MSConversation) {
        savedConversation = conversation
    }
    
    @IBAction func sendButtonTapped(_ sender: Any) {
        if messageTextView.textColor != UIColor.lightGray {
            savedConversation?.sendText(messageTextView.text, completionHandler: nil)
            messageTextView.text = ""
            self.textViewDidChange(messageTextView)
        }
    }
    
    @IBAction func emotionButtonTapped(_ sender: Any) {
        guard let button = sender as? UIButton else {
            return
        }
        
        var emotion = "empty"
        
        switch button.tag {
        case 1:
            emotion = "happiness"
        case 2:
            emotion = "sadness"
        case 3:
            emotion = "love"
        case 4:
            emotion = "surprise"
        case 5:
            emotion = "hatred"
        case 6:
            emotion = "boredom"
        case 7:
            emotion = "worry"
        case 8:
            emotion = "relief"
        case 9:
            emotion = "fun"
        case 10:
            emotion = "anger"
        case 11:
            emotion = "excitement"
        case 12:
            emotion = "neutrality"
        default: break
        }
        
        statusLabel.text = "Intentions will help you convey " + emotion
        
        if self.presentationStyle != .expanded {
            self.requestPresentationStyle(.expanded)
        }
    }
    
}

extension MessagesViewController: UITextViewDelegate {
    func textViewDidChange(_ textView: UITextView) {
        // Add placeholder if there is no text.
        if textView.text == "" {
            messageTextView.text = messagePlaceholder
            messageTextView.textColor = UIColor.lightGray
            messageTextView.becomeFirstResponder()
            messageTextView.selectedTextRange = messageTextView.textRange(from: messageTextView.beginningOfDocument, to: messageTextView.beginningOfDocument)
        } else if textView.textColor == UIColor.lightGray && textView.text != messagePlaceholder {
            textView.textColor = UIColor.black
            textView.text = textView.text.replacingOccurrences(of: messagePlaceholder, with: "")
        }
        
        // Adjust text view height.
        let fixedWidth = textView.frame.size.width
        let currentHeight = textView.frame.size.height
        let newSize = textView.sizeThatFits(CGSize(width: fixedWidth, height: CGFloat.greatestFiniteMagnitude))
        
        // Check if text view is growing or shrinking.
        if currentHeight > newSize.height || (currentHeight < newSize.height && messageViewHeightLayoutConstraint.constant < 108.0) {
            textView.frame.size = CGSize(width: max(newSize.width, fixedWidth), height: newSize.height)
            
            // Adjust parent view height.
            messageViewHeightLayoutConstraint.constant = newSize.height + 20.0
            
            // Set scrolling.
            messageTextView.isScrollEnabled = messageViewHeightLayoutConstraint.constant == 108.0
        }
        
        // Perform emotion analysis.
        if letterCounter % frequency == 0 {
            EmotionService.emotion(text: messageTextView.text) { result in
                guard let result = result else { return }
                
                print(result)
            }
        }
        
        letterCounter += 1
    }

    func textViewDidChangeSelection(_ textView: UITextView) {
        if textView.textColor == UIColor.lightGray {
            textView.selectedTextRange = textView.textRange(from: textView.beginningOfDocument, to: textView.beginningOfDocument)
        }
    }
}
