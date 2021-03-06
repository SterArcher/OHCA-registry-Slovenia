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
        db_table = 'systems'

class CaseReport(models.Model):
    caseID = models.CharField(max_length = 32, primary_key = True)
    dispatchID = models.CharField(max_length = 32, blank = True, null = True, unique = True)
    systemID = models.ForeignKey(System, on_delete = models.DO_NOTHING)
    localID = models.ForeignKey(Locale, on_delete = models.DO_NOTHING)
    dispIdentifiedCA = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    dispProvidedCPRinst = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    age = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(200)])
    gender = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    witnesses = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    location  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])
    bystanderResponse = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderResponseTime = models.BigIntegerField(null = True, blank = True, validators=[MaxValueValidator(-1)])
    bystanderAED = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    bystanderAEDTime = models.BigIntegerField(null = True, blank = True, validators=[MaxValueValidator(-1)])
    deadOnArrival = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    firstMonitoredRhy = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    pathogenesis = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(1), MaxValueValidator(6)])
    independentLiving = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    comorbidities = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    vad = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cardioverterDefib = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    stemiPresent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    responseTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    defibTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ttm = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    ttmTemp =models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(400)])
    drugs = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(7)])
    airwayControl = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(15)])
    cprQuality = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    shocks = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    drugTimings = models.JSONField(default = dict)
    vascularAccess = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(4)])
    mechanicalCPR = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    targetVent = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(3)])
    reperfusionAttempt = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(8)])
    reperfusionTime = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ecls = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(2)])
    iabp = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ph = models.DecimalField(max_digits = 5, decimal_places = 3, null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(14)])
    lactate = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    glucose = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    neuroprognosticTests = models.JSONField(default = dict)
    specialistHospital  = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    hospitalVolume = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    ecg = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    ecgBLOB = models.FileField(null = True, blank = True)
    targetBP = models.DecimalField(max_digits = 10, decimal_places = 5, null = True, blank = True, validators=[MinValueValidator(-1)])
    survived = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    rosc = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    roscTime = models.BigIntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    SurvivalDischarge30d = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    cpcDischarge = models.SmallIntegerField( null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(5)])
    mrsDischarge = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(6)])
    survivalStatus = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    transportToHospital = models.SmallIntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    treatmentWithdrawn = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1)])
    cod = models.CharField(max_length = 6, null = True, blank = True)
    organDonation = models.IntegerField(null = True, blank = True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    patientReportedOutcome = models.SmallIntegerField(null = True, blank = True)
    qualityOfLife = models.JSONField(default = dict)
    
    def update(self, *args, **kwargs):
        for name,values in kwargs.items():
            if not(name == 'caseID'):
                try:
                    setattr(self,name,values)
                except KeyError:
                    pass
        self.save()
        return True

    def __str__(self):
        return self.caseID
    
    class Meta:
        db_table = 'cases'