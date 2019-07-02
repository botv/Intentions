//
//  ExpandedViewController.swift
//  Intentions MessagesExtension
//
//  Created by Ben Botvinick on 12/1/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import UIKit
import Messages
import UITextView_Placeholder

class ExpandedViewController: MSMessagesAppViewController {

    @IBOutlet weak var messageViewHeightConstraint: NSLayoutConstraint!
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var inputContainerView: UIView!
    
    // Emotion buttons
    @IBOutlet weak var happyEmotionButton: UIButton!
    @IBOutlet weak var sadEmotionButton: UIButton!
    @IBOutlet weak var loveEmotionButton: UIButton!
    @IBOutlet weak var surpriseEmotionButton: UIButton!
    @IBOutlet weak var hateEmotionButton: UIButton!
    @IBOutlet weak var boredEmotionButton: UIButton!
    @IBOutlet weak var worriedEmotionButton: UIButton!
    @IBOutlet weak var relievedEmotionButton: UIButton!
    @IBOutlet weak var funEmotionButton: UIButton!
    @IBOutlet weak var angerEmotionButton: UIButton!
    @IBOutlet weak var excitedEmotionButton: UIButton!
    @IBOutlet weak var neutralEmotionButton: UIButton!
    
    // Message input text view setup
    @IBOutlet weak var messageTextView: UITextView! {
        didSet {
            // Round corners.
            messageTextView.layer.cornerRadius = 20.0
            messageTextView.layer.masksToBounds = true
            messageTextView.layer.borderWidth = 0.5
            messageTextView.layer.borderColor = UIColor.lightGray.cgColor
            
            // Set up padding.
            messageTextView.textContainerInset = UIEdgeInsets(top: 8, left: 10.0, bottom: 8, right: 40.0);
            
            // Set up placeholder
            messageTextView.placeholder = "iMessage"
        }
    }
    
    var savedConversation: MSConversation?
    var messagePlaceholder = "iMessage"
    var letterCounter = 0
    let frequency = 8
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set up multiline label
        statusLabel.sizeToFit()
        
        // Align text input to keyboard top
        inputContainerView.bottomAnchor.constraint(equalTo: view.keyboardLayoutGuide.topAnchor).isActive = true
        
        // Hide the keyboard when the user clicks on the screen
        self.hideKeyboardWhenTappedAround()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewDidLayoutSubviews()
        
        requestPresentationStyle(.expanded)
    }
    
    override func didTransition(to presentationStyle: MSMessagesAppPresentationStyle) {
        if presentationStyle == .expanded {
            self.view.isHidden = false
            inputContainerView.becomeFirstResponder()
            view.layoutIfNeeded()
        }
    }

    @IBAction func doneButtonTapped(_ sender: Any) {
        if messageTextView.textColor != UIColor.lightGray {
            savedConversation?.insertText(messageTextView.text, completionHandler: nil)
            messageTextView.text = ""
            self.textViewDidChange(messageTextView)
            self.dismiss()
        }
        
        print(messageTextView.text)
    }
}

extension ExpandedViewController: UITextViewDelegate {
    func textViewDidChange(_ textView: UITextView) {
        
        // Adjust text view height.
        let fixedWidth = textView.frame.size.width
        let currentHeight = textView.frame.size.height
        let newSize = textView.sizeThatFits(CGSize(width: fixedWidth, height: CGFloat.greatestFiniteMagnitude))
        
        // Check if text view is growing or shrinking.
        if currentHeight > newSize.height || (currentHeight < newSize.height && messageViewHeightConstraint.constant < 108.0) {
            textView.frame.size = CGSize(width: max(newSize.width, fixedWidth), height: newSize.height)
            
            // Adjust parent view height.
            messageViewHeightConstraint.constant = newSize.height + 20.0
            
            // Set scrolling.
            messageTextView.isScrollEnabled = messageViewHeightConstraint.constant == 108.0
        }
        
        // Perform emotion analysis.
        if letterCounter % frequency == 0 {
            EmotionService.emotion(text: messageTextView.text) { result in
                guard let result = result else { return }
                
                self.statusLabel.text = EmotionService.sentence(emotion: result)
                
                switch result {
                case "Bored":
                    self.boredEmotionButton.wiggle()
                case "Sarcasm":
                    self.funEmotionButton.wiggle()
                case "Angry":
                    self.angerEmotionButton.wiggle()
                case "Sad":
                    self.sadEmotionButton.wiggle()
                case "Fear":
                    self.worriedEmotionButton.wiggle()
                case "Excited":
                    self.excitedEmotionButton.wiggle()
                case "Happy":
                    self.happyEmotionButton.wiggle()
                default: break
                }
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
