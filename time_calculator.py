def add_time(start, duration, week=None):
    days_weeks = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    start_hour,start_minutes = start.split(":")
    operator = start.split(" ")[1]
    duration_hour,duration_minutes = duration.split(":")
    
    #Calcula os minutos, se for mair que 59, aumenta mais uma hora e diminui os minutos
    def calculateMinutes (hour,minutes):
        while minutes > 59:
            hour = hour + 1
            minutes = minutes - 60
            if minutes == 0:
                minutes = minutes + 1
        return hour, minutes
    
    #Calcula se é AM ou PM atráves de par ou impar
    def meridiemCalculator(meridiem = "AM", days_of_calculate = 0):
        meridiem_dict = {
            0 : "AM",
            1 : "PM"
        }        

        meridiem_res = meridiem_dict[days_of_calculate%2] if meridiem == "AM" else meridiem_dict[(days_of_calculate + 1)%2]
        return meridiem_res

    #Transforma as horas (12 horas) em 1 dia judaico (12 horas). Cada dia é 12 horas
    def daysInTwelveHours (hours=0,minutes=0):
        days = 0
        while hours > 12:
            days = days + 1
            hours = hours - 12
        if hours == 12 and minutes > 0:
            days = days + 1    
        return hours,days
    
    #Calcula o dia da semana baseado no index de cada dia da semana
    def daysOfTheWeek (days_in_twelve_Hours=None,day_week="sunday",post_meridiem=False):
        day_in_twenty_four = int((days_in_twelve_Hours /2)+0.5) if post_meridiem == True else int(days_in_twelve_Hours/2)
        index_week = days_weeks.index(day_week.lower())
         
        fill = (index_week + day_in_twenty_four)
        while fill > 6:
            fill = fill - len(days_weeks)       
        
        return days_weeks[fill]
    
    #Retorna uma string formatada no padrão do teste
    def messageReturns (days, hour, minutes, operator=None, day_week=None):
        next_day=""
        if day_week:
            str_week = f", {day_week.title()} "
        
        else:
            str_week = " "
            
        if days == 0:
            str_return = f"{hour}:{minutes} {operator}{str_week}".strip()
        
        elif days > 0 and days < 3:
            if operator == "PM" and days == 1: 
                next_day="(next day)"
            
            elif operator == "AM" and days == 2:
                next_day="(next day)"
                
            str_return = f"{hour}:{minutes} {operator}{str_week}{next_day}".strip()
        
        else:
            str_return = f"{hour}:{minutes} {operator}{str_week}({int(days/2)+1} days later)".strip()

        return str_return
    
    #Realiza a soma dos valores de entreda (hh:mm inicial + hh:mm pra calcular) 
    hour,minutes=calculateMinutes(
        int(start_hour)+int(duration_hour),
        int(start_minutes.replace(operator,""))+int(duration_minutes)
    )
    
    #Transforma as horas em dias
    hour,days = daysInTwelveHours(hour,minutes)
    
    #Calcula se é AM/PM 
    new_operator = meridiemCalculator(operator,days)
    
    #Se não for None, calcula o novo dia da semana
    if week:
        week = daysOfTheWeek(days,week.lower(),(operator == "PM"))

    #Recebe a string formatada para o retorno da função    
    new_time = messageReturns(days,hour,str(minutes).rjust(2,"0"),operator,week)
    
    #Altera para o novo operator (AM/PM) se teve alteração
    new_time = new_time.replace(operator,new_operator)
    
    return new_time