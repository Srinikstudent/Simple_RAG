import spacy

nlp = spacy.load("en_core_web_sm")

def extract_rules(text):
    doc = nlp(text)

    str = ""
    amount = None
    for token in doc:
        if token.ent_type_ == "MONEY":
            amount = float(token.text.replace(",", ""))
            break
        if token.text.upper() == "RECURRING":
            str = "RECURRING"
            break
        if token.text.upper() == "TRADER":
            str = "TRADER"
            break
        if token.text.upper() == "TRUST":
            str = "TRUST"
            break
        if token.text.upper() == "INCORPORATED":
            str = "INCORPORATED"
            break
        if token.text.upper() == "COOPERATIVE":
            str = "COOPERATIVE"
            break
        if token.text.upper() == "DOMESTIC":
            str = "DOMESTIC"
            break
        if token.text.upper() == "REGISTERED":
            str = "REGISTERED"
            break
        if token.text.upper() == "UNREGISTERED":
            str = "UNREGISTERED"
            break

    
    if amount and amount < 10000:
        return ["customer's name", "customer's residential address", "customer's date of birth",
                "any other name that the customer is known by", "customer's country(ies) of citizenship",
                "customer's country(ies) of residence", "requesting PAN number" ,"customer's occupation or business activities",
                "nature of the customer's business with the reporting entity", "income or assets available to the customer",
                "customer's source of funds including the origin of funds", "customer's financial position",
                "beneficial ownership of the funds used by the customer with respect to the designated services",
                "beneficiaries of the transactions being facilitated by the reporting entity on behalf of the customer including the destination of funds"]
    elif amount and amount >= 10000:
        return ["customer’s name", "residential address", 
                "source of funds including the origin of funds",
                "occupation or business activities and purpose of transaction", "the customer’s country(ies) of citizenship",
                "the customer’s country(ies) of residence must be disclosed"]
    elif str == "RECURRING":
        return [ "justifiable documents from the sending and receiving ends", 
                "along with the source of funds and the latest bank statement must be disclosed"]
    elif str == "TRADER":
         return ["the full name as registered in ASIC",
                 "address of the company", "principal place of operation", 
                 "nature of business by the company and type of company (proprietary or public) must be disclosed"]
    elif str == "TRUST":
        return ["full name of the trust", "the type of trust", "country of establishment",
                "and information if any of the trustees is an individual or a company must be disclosed"]
    elif str == "INCORPORATED":
        return ["the full name of the association", "full address of the head office",
                "unique identification number", "the State, Territory", "or Country in which the association was incorporated", 
                "the date upon which the association was incorporated", "the full name of the chairman",
                "and the objects of the association must be disclosed"]
    elif str == "COOPERATIVE":
        return ["the full name of the cooperative", "full address of the head office", 
                "unique identification number", "the State, Territory", "or Country in which the cooperative was incorporated",
                "the date upon which the cooperative was incorporated", "the full name of the chairman",
                "and the objects of the cooperative must be disclosed"]
    elif str == "DOMESTIC":
        return ["the full name of the company",
                "and the information of the company being in an official list of a domestic stock exchange must be disclosed"]
    elif str == "REGISTERED":
        return ["the full name of the company", "the information of the company being in an official list of a domestic stock exchange",
                "and the information of the company whose shares", "in whole or in part", 
                "are listed for quotation in the official list of any stock or equivalent exchange must be disclosed"]
    elif str == "UNREGISTERED":
        return ["the information of the company whose shares", "in whole or in part",
                "are listed for quotation in the official list of any stock or equivalent exchange disclosed"]