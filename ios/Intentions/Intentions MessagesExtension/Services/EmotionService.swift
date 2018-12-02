//
//  EmotionService.swift
//  Intentions MessagesExtension
//
//  Created by Ben Botvinick on 12/2/18.
//  Copyright © 2018 Ben Botvinick. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON

struct EmotionService {
    static func sentence(emotion: String) -> String {
        switch emotion {
        case "Bored": return "You sound bored :|"
        case "Sarcasm": return "You sound sarcastic ;/"
        case "Angry": return "You sound angry >:("
        case "Sad": return "You sound sad :("
        case "Fear": return "You sound scared :o"
        case "Excited": return "You sound excited :D"
        case "Happy": return "You sound happy :)"
        default: return "Type something to know how you sound."
        }
    }
    
    static func emotion(text: String, completion: @escaping (String?) -> Void) {
        let parameters: Parameters = [
            "api_key": "Pc95sWKl9x1WUpjS8dZvyjNZnt6TNSRtkem3qSOlVcI",
            "text": text
        ]
        
        let url = "https://apis.paralleldots.com/v3/emotion"
        
        Alamofire.request(url, method: .post, parameters: parameters).validate().responseJSON { response in
            switch response.result {
            case .success:
                let json = JSON(response.value!)
                print(json)
                let emotion = json["emotion"]["emotion"].string
                completion(emotion)
            case .failure(let error):
                print(error)
                completion(nil)
            }
        }
    }
}
