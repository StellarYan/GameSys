function input_mask() {
    Inputmask("9-a{1,3}9{1,3}").mask("#ID");
    Inputmask("9", { repeat: 10 }).mask("#MatchID");
    Inputmask({ regex: "\\d*" }).mask("#PlayerID");
    Inputmask({ regex: String.raw`\d*` }).mask("#DScore");
    Inputmask({ regex: String.raw`\d*` }).mask("#PScore");
    Inputmask({ regex: String.raw`\d*` }).mask("#JudgeID");
    Inputmask({ regex: String.raw`\d*` }).mask("#Score");
    Inputmask({ regex: String.raw`\d*` }).mask("#IsChief");
    Inputmask({ regex: String.raw`\d*` }).mask("#Group");
    Inputmask({ regex: String.raw`\d*` }).mask("#Event");
    Inputmask({ regex: String.raw`\d*` }).mask("#ChiefID");
    Inputmask({ regex: String.raw`\d*` }).mask("#StartTime");
    Inputmask({ regex: String.raw`\d*` }).mask("#EndTime");
    Inputmask({ regex: String.raw`\d*` }).mask("#Name");
    Inputmask({ regex: String.raw`\d*` }).mask("#Gender");
    Inputmask({ regex: String.raw`\d*` }).mask("#PhoneNum");
    Inputmask({ regex: String.raw`\d*` }).mask("#Age");
    Inputmask({ regex: String.raw`\d*` }).mask("#CultureScore");
    Inputmask({ regex: String.raw`\d*` }).mask("#MatchType");
}