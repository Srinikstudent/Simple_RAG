import spacy

nlp = spacy.load('en_core_web_sm')

def extract_rules(text):
    doc = nlp(text)

    str = ""
    name = ""
    is_person = False
    amount = None
    
    for token in doc.ents:
        print(token.text)
        
        if token.label_ == "PERSON":
            name = token.text
            is_person = True
            
        if token.label_ == "ORG":
            name = token.text
        
        if token.label_ == "MONEY":
            amount = float(token.text.replace(",", ""))
            break
        
        
    for token in doc:
        
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

    
    if amount and amount < 10000 and is_person:
        return (["full_cust_names", "residential_address", "country_of_citizenship",
                "customer_of_residence","occ_business_act", "purpose_of_transaction", 
                "source_of_funds"], name)
        
    elif amount and amount >= 10000 and is_person:
        return (["full_cust_names", "residential_address", "source_of_funds",
                "occ_business_act", "purpose_of_transaction", "country_of_citizenship",
                "country_of_residence"], name)
    
    elif str == "RECURRING":
        return (["occ_business_act", "purpose_of_transaction", "source_of_funds"], name)
    
    elif str == "TRADER":
         return (["full_cust_names",
                 "address_of_company", "principal_place_of_operation", 
                 "nature_of_business_by_the_company_and_type_of_company"], name)
                 
    elif str == "TRUST":
        return (["full_cust_names", "type_of_trust", "country_of_establishment",
                "any_trustee_is_individual_or_company"], name)
                 
    elif str == "INCORPORATED":
        return (["full_cust_names", "full_address_of_the_head_office",
                "unique_identification_number", "State_Country_Territory_of_incorporation", 
                "date_of_incorporation", "name_of_chairman", "objects_of_entity"], name)
    
    elif str == "COOPERATIVE":
        return (["full_cust_names", "full_address_of_the_head_office", 
                "unique identification number", "State_Country_Territory_of_incorporation",
                "date_of_incorporation", "name_of_chairman", "objects_of_entity"], name)
    
    elif str == "DOMESTIC":
        return (["full_cust_names", "info_in_domestic_exchange"], name)
    
    elif str == "REGISTERED":
        return (["full_cust_names", "info_in_domestic_exchange", "info_in_official_exchange"], name)
    
    elif str == "UNREGISTERED":
        return (["info_in_official_exchange"], name)
    
    else :
        return(["full_cust_names", "country_of_establishment", "occ_business_act", "purpose_of_transaction", "source_of_funds"], name)