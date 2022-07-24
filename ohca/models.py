#from asyncio.windows_events import NULL
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Locale(models.Model):
    localID = models.BigAutoField(primary_key=True)
    friendlyName = models.TextField()
    population = models.IntegerField(default = 0)
    attendedCAs = models.IntegerField(default = 0)
    attemptedResusc = models.IntegerField(default = 0)
    casesDNR = models.IntegerField(default = 0)
    casesFutile = models.IntegerField(default = 0)
    casesCirculation = models.IntegerField(default = 0)
    casesUnknown = models.IntegerField(default = 0)
    description = models.JSONField(default = dict)
    descriptionSupplemental = models.TextField(null = True, blank = True)
    
    def update(self, *args, **kwargs):
        for name,values in kwargs.items():
            if not(name == 'localID'):
                try:
                    setattr(self,name,values)
                except KeyError:
                    pass
        self.save()
        return True

    def __str__(self):
        return self.friendlyName

    class Meta:
        ordering = ('friendlyName',) # orders them alphabetically in drop down menu
        db_table = 'locales'

class System(models.Model):
    systemID = models.BigAutoField(primary_key=True)
    friendlyName = models.TextField()
    population = models.IntegerField(default = 0)
    attendedCAs = models.IntegerField(default = 0)
    attemptedResusc = models.IntegerField(default = 0)
    casesDNR = models.IntegerField(default = 0)
    casesFutile = models.IntegerField(default = 0)
    casesCirculation = models.IntegerField(default = 0)
    casesUnknown = models.IntegerField(default = 0)
    description = models.JSONField(default = dict)
    descriptionSupplemental = models.TextField(null = True, blank = True)
    
    def update(self, *args, **kwargs):
        for name,values in kwargs.items():
            if not(name == 'systemID'):
                try:
                    setattr(self,name,values)
                except KeyError:
                    pass
        self.save()
        return True

    def __str__(self):
        return self.friendlyName
    
    class Meta:
        ordering = ('friendlyName',) # orders them alphabetically in drop down menu
        db_table = 'systems'

class CaseReport(models.Model):
    numID = models.BigAutoField(primary_key=True)
    caseID = models.CharField(max_length = 64, blank = True, null = True, db_index = True) 
    dispatchID = models.CharField(max_length = 64, blank = True, null = True, db_index = True)
    systemID = models.ForeignKey(System, on_delete = models.DO_NOTHING)
    localID = models.ForeignKey(Locale, on_delete = models.DO_NOTHING)

    interventionID = models.CharField(max_length=12, blank = True, null = True) 
    mainInterventionID = models.CharField(max_length=12, blank = True, null = True) 

    dispIdentifiedCA = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    dispProvidedCPRinst = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    callTimestamp = models.DateTimeField(null = True, blank = True)

    age = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(200)])
    gender = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    witnesses = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    location  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])

    CAtimestamp = models.DateTimeField(null=True, blank=True) # time of CA
    estimatedCAtimestamp = models.BooleanField(null=True, blank=True) # was the time estimated or not?

    bystanderResponse = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderResponseTime = models.BigIntegerField(null = True, blank = True)
    bystanderResponseTimestamp = models.DateTimeField(null = True, blank = True)

    bystanderAED = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderAEDTime = models.BigIntegerField(null = True, blank = True),
    bystanderAEDTimestamp = models.DateTimeField(null = True, blank = True)

    deadOnArrival = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    diedOnField = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)]) # ali je bolnik umrl na terenu

    firstMonitoredRhy = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(7)])
    pathogenesis = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(1), MaxValueValidator(6)])
    independentLiving = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    comorbidities = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    vad = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cardioverterDefib = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    stemiPresent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])

    
    responseTime = models.BigIntegerField(null = True, blank = True)
    # # responseTime = models.TimeField(null = True, blank = True)
    responseTimestamp = models.DateTimeField(null = True, blank = True)

    defibTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    # # defibTime = models.TimeField(null = True, blank = True)
    defibTimestamp = models.DateTimeField(null = True, blank = True)
    firstDefibWho = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)]) 

    ttm = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    ttmTemp =models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(400)])
    drugs = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(7)])
    airwayControl = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(15)])
    cprQuality = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    shocks = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    
    drugTimings = models.BigIntegerField(null = True, blank = True) # time interval from incoming call to the time vascular acces is obtained and the first drug is given
    drugTimingsTimestamp = models.DateTimeField(null = True, blank = True)
    
    vascularAccess = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    mechanicalCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    targetVent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    reperfusionAttempt = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])
    reperfusionTime = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    # # reperfusionTime = models.TimeField(null = True, blank = True)
    reperfusionTimestamp = models.DateTimeField(null = True, blank = True)

    ecls = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    iabp = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ph = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(14)], help_text = "Zaokrožite na dve decimalki.")
    lactate = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    glucose = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    
    neuroprognosticTests = models.TextField(null = True, blank = True)
    specialistHospital  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    hospitalName = models.CharField(null=True, blank=True, max_length=1000) # če bomo hoteli določit obremenitev bomo rabili vedet katera bolnica je? Najbrž isto kot pri systemID
    
    hospitalVolume = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ecg = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ecgBLOB = models.FileField(null = True, blank = True)
    targetBP = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    survived = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    rosc = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    roscTime = models.BigIntegerField(null = True, blank = True)
    roscTimestamp = models.DateTimeField(null = True, blank = True)

    # # ločimo survivalDischarge in survival30d -> iz tega potem dobimo survivalDischarge30d
    survivalDischarge = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    survival30d = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    SurvivalDischarge30d = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])

    cpcDischarge = models.SmallIntegerField( null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    mrsDischarge = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(6)])
    survivalStatus = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    transportToHospital = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    treatmentWithdrawn = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    treatmentWithdrawnTimestamp = models.DateTimeField(null = True, blank = True)
    cod = models.CharField(max_length = 6, null = True, blank = True)
    organDonation = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])

    patientReportedOutcome = models.TextField(null = True, blank = True)
   
    qualityOfLife = models.TextField(null = True, blank = True)

    reaLand = models.CharField(null = True, blank = True, max_length=200) # spremenila iz intergerfield na charfield
    reaRegion = models.CharField(null = True, blank = True, max_length=200)
    # reaLand = models.SmallIntegerField(null = True, blank = True)
    # reaRegion = models.SmallIntegerField(null = True, blank = True)
    reaConf = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cprEms = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cPREMS3Time = models.IntegerField(null = True, blank = True)
    #cPREMS3Timestamp = models.DateTimeField(null = True, blank = True)
    noCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    # # patID = None # NULL, TODO?
    reaYr = models.SmallIntegerField(null = True, blank = True)
    reaMo = models.SmallIntegerField(null = True, blank = True)
    reaDay = models.SmallIntegerField(null = True, blank = True)
    reaTime = models.IntegerField(null = True, blank = True)
    reaTimestamp = models.DateTimeField(null = True, blank = True)
    reaCause = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    timeTCPR = models.IntegerField(null = True, blank = True)
    timestampTCPR = models.DateTimeField(null = True, blank = True)
    gbystnader = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ageBystander = models.SmallIntegerField(null = True, blank = True)
    estimatedAgeBystander = models.BooleanField(null=True, blank=True)
    cPRbystander3Time = models.IntegerField(null = True, blank = True)
    cPRbystander3Timestamp = models.DateTimeField(null = True, blank = True)
    helperCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    helperWho = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    #persCPRstart = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    
    cPRhelper3Time = models.IntegerField(null = True, blank = True)
    cPRhelper3Timestamp = models.DateTimeField(null = True, blank = True)
    defiOrig = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    timeROSC = models.IntegerField(null = True, blank = True)
    timestampROSC = models.DateTimeField(null = True, blank = True)
    endCPR4Time = models.IntegerField(null = True, blank = True)
    endCPR4Timestamp = models.DateTimeField(null = True, blank = True)
    leftScene5Time = models.IntegerField(null = True, blank = True)
    leftScene5Timestamp = models.DateTimeField(null = True, blank = True)
    hospitalArrival6Time = models.IntegerField(null = True, blank = True)
    hospitalArrival6Timestamp = models.DateTimeField(null = True, blank = True)
    hospArri = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    dischDay = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(31)])
    dischMonth = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(12)])
    dischYear = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    #discDate = models.DateField(null = True, blank = True)

    def update(self, *args, **kwargs):
        for name,values in kwargs.items():
            if not(name == 'caseID'):
                try:
                    setattr(self,name,values)
                except KeyError:
                    pass
        self.save()
        return True

    # TODO
    # def __str__(self):
    #     return self.caseID
    
    class Meta:
        db_table = 'cases'

class ICD(models.Model):
    code = models.CharField(primary_key=True, max_length=6)
    chapter = models.SmallIntegerField()
    category = models.CharField(max_length=3)
    subcategory4 = models.SmallIntegerField(null = True, blank = True)
    subcategory5 = models.SmallIntegerField(null = True, blank = True)
    rank1 = models.CharField(max_length=6)
    rank2 = models.CharField(max_length=6, null = True, blank = True)
    rank3 = models.CharField(max_length=6, null = True, blank = True)
    level = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    slovenian = models.TextField()
    english = models.TextField()
    valid = models.BooleanField()
    group = models.SmallIntegerField()

    class Meta:
        db_table = 'icd-10-am'