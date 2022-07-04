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
    dispIdentifiedCA = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    dispProvidedCPRinst = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    age = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(200)])
    gender = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    witnesses = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    location  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])
    bystanderResponse = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderResponseTime = models.TimeField(null = True, blank = True)
    #bystanderResponseTime = models.BigIntegerField(null = True, blank = True, validators=[MaxValueValidator(-1)])
    bystanderAED = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderAEDTime = models.TimeField(null = True, blank = True)
    #bystanderAEDTime = models.BigIntegerField(null = True, blank = True, validators=[MaxValueValidator(-1)])
    deadOnArrival = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    firstMonitoredRhy = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    pathogenesis = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(1), MaxValueValidator(6)])
    independentLiving = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    comorbidities = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    vad = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cardioverterDefib = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    stemiPresent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    responseTime = models.BigIntegerField(null = True, blank = True)
    #responseTime = models.TimeField(null = True, blank = True, validators=[MinValueValidator(-1)])
    defibTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ttm = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    ttmTemp =models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(400)])
    drugs = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(7)])
    airwayControl = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(15)])
    cprQuality = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    shocks = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    drugTimings = models.JSONField(null = True, blank = True, default = dict)
    vascularAccess = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    mechanicalCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    targetVent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    reperfusionAttempt = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])
    reperfusionTime = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ecls = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    iabp = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ph = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(14)], help_text = "Zaokrožite na dve decimalki.")
    lactate = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    glucose = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    neuroprognosticTests = models.JSONField(null = True, blank = True, default = dict)
    specialistHospital  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    hospitalVolume = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ecg = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ecgBLOB = models.FileField(null = True, blank = True)
    targetBP = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    survived = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    rosc = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    roscTime = models.TimeField(null = True, blank = True)
    # roscTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    SurvivalDischarge30d = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cpcDischarge = models.SmallIntegerField( null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    mrsDischarge = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(6)])
    survivalStatus = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    transportToHospital = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    treatmentWithdrawn = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    cod = models.CharField(max_length = 6, null = True, blank = True)
    organDonation = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    patientReportedOutcome = models.SmallIntegerField(null = True, blank = True)
    qualityOfLife = models.JSONField(null = True, blank = True, default = dict)
    reaLand = models.SmallIntegerField(null = True, blank = True)
    reaRegion = models.SmallIntegerField(null = True, blank = True)
    reaConf = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cprEms = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cPREMS3Time = models.IntegerField(null = True, blank = True)
    noCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    # patID = None # NULL, TODO?
    reaYr = models.SmallIntegerField(null = True, blank = True)
    reaMo = models.SmallIntegerField(null = True, blank = True)
    reaDay = models.SmallIntegerField(null = True, blank = True)
    reaTime = models.IntegerField(null = True, blank = True)
    reaCause = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    timeTCPR = models.IntegerField(null = True, blank = True)
    gbystnader = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ageBystander = models.SmallIntegerField(null = True, blank = True)
    estimatedAgeBystander = models.BooleanField(null=True, blank=True)
    cPRbystander3Time = models.IntegerField(null = True, blank = True)
    helperCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    helperWho = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    cPRhelper3Time = models.IntegerField(null = True, blank = True)
    defiOrig = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    timeROSC = models.IntegerField(null = True, blank = True)
    endCPR4Time = models.IntegerField(null = True, blank = True)
    leftScene5Time = models.IntegerField(null = True, blank = True)
    hospitalArrival6Time = models.IntegerField(null = True, blank = True)
    hospArri = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    dischDay = models.SmallIntegerField(null = True, blank = True)
    #dischDay = models.DateField(null = True, blank = True, auto_now=False, auto_now_add=False)

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
