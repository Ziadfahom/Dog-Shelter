class DogSerializer:
    """
    Serializer class for handling the serialization of the Dog model
    and related models such as Owner and Entrance Examination for JSON exporting.
    """
    @staticmethod
    def serialize_owner(owner_obj):
        """
        Serialize owner object to a dictionary.

        :param owner_obj: Owner object
        :type owner_obj: Owner model instance or None
        :return: Serialized owner data or None if owner_obj is None
        :rtype: dict or None
        """

        if not owner_obj:
            return None
        return {
            'ownerSerialNum': owner_obj.ownerSerialNum,
            'firstName': owner_obj.firstName,
            'lastName': owner_obj.lastName,
            'ownerID': owner_obj.ownerID,
            'ownerAddress': owner_obj.ownerAddress,
            'city': owner_obj.city,
            'phoneNum': owner_obj.phoneNum,
            'cellphoneNum': owner_obj.cellphoneNum,
            'comments': owner_obj.comments
        }

    @staticmethod
    def serialize_entrance_examinations(examinations):
        """
        Serialize a list of EntranceExamination objects to dictionaries.

        :param examinations: List of EntranceExamination objects
        :type examinations: list
        :return: List of serialized examination data
        :rtype: list
        """

        return [
            {
                'examinationID': exam.examinationID,
                'examinationDate': exam.examinationDate,
                'examinedBy': exam.examinedBy,
                'results': exam.results,
                'dogWeight': exam.dogWeight,
                'dogTemperature': exam.dogTemperature,
                'dogPulse': exam.dogPulse,
                'comments': exam.comments
            } for exam in examinations
        ]

    @staticmethod
    def serialize_treatments(treatments):
        """
        Serialize a list of Treatment objects to dictionaries.

        :param treatments: List of Treatment objects
        :type treatments: list
        :return: List of serialized treatment data
        :rtype: list
        """

        return [
            {
                'treatmentID': treatment.treatmentID,
                'treatmentName': treatment.treatmentName,
                'treatmentDate': treatment.treatmentDate,
                'treatedBy': treatment.treatedBy,
                'comments': treatment.comments
            } for treatment in treatments
        ]

    @staticmethod
    def serialize_dog_stances(dog_stances):
        """
        Serialize a list of DogStance objects to dictionaries.

        :param dog_stances: List of Dog Stance objects
        :type dogStance: list
        :return: List of serialized dogStance data
        :rtype: list
        """
        return [
            {
                'stanceStartTime': stance.stanceStartTime,
                'dogStance': stance.dogStance,
                'dogLocation': stance.dogLocation,
            } for stance in dog_stances
        ]

    @staticmethod
    def serialize_observations(observations):
        """
        Serialize a list of Observation objects to dictionaries.

        :param observations: List of Observation objects
        :type observations: list
        :return: List of serialized observation data
        :rtype: list
        """
        return [
            {
                'obsDateTime': observation.obsDateTime,
                'sessionDurationInMins': observation.sessionDurationInMins,
                'isKong': observation.isKong,
                'jsonFile': str(observation.jsonFile),
                'rawVideo': str(observation.rawVideo),
                'dogStances': DogSerializer.serialize_dog_stances(observation.dogstance_set.all()),

            } for observation in observations
        ]

    @staticmethod
    def serialize_observes(observes):
        """
        Serialize a list of Observes objects to dictionaries.

        :param observes: List of Observes objects
        :type observes: list
        :return: List of serialized observes data
        :rtype: list
        """

        return [
            {
                'camID': observe.camera.camID,
                'sessionDate': observe.sessionDate,
                'comments': observe.comments,
                'observations': DogSerializer.serialize_observations(observe.observation_set.all())

            } for observe in observes
        ]

    @staticmethod
    def serialize_dog_placements(placements):
        """
        Serialize a list of DogPlacement objects to dictionaries.

        :param placements: List of DogPlacement objects
        :type placements: list
        :return: List of serialized dog placements data
        :rtype: list
        """

        return [
            {
                'kennelNum': placement.kennel.kennelNum,
                'kennelImage': str(placement.kennel.kennelImage),
                'entranceDate': placement.entranceDate,
                'expirationDate': placement.expirationDate,
                'placementReason': placement.placementReason
            } for placement in placements
        ]

    @classmethod
    def serialize_dog(cls, dog):
        """
        Serialize a Dog object including related models.

        :param dog: Dog object
        :type dog: Dog model instance
        :return: Serialized Dog data
        :rtype: dict
        """

        dog_fields = {
            'dogID': dog.dogID,
            'chipNum': dog.chipNum,
            'dogName': dog.dogName,
            'dateOfBirthEst': dog.dateOfBirthEst,
            'dateOfArrival': dog.dateOfArrival,
            'dateOfVaccination': dog.dateOfVaccination,
            'breed': dog.breed,
            'gender': dog.gender,
            'furColor': dog.furColor,
            'isNeutered': dog.isNeutered,
            'isDangerous': dog.isDangerous,
            'dogImage': str(dog.dogImage),
            'kongDateAdded': dog.kongDateAdded,

            # Include associated entities
            'owner': cls.serialize_owner(dog.owner),
            'entranceExaminations': cls.serialize_entrance_examinations(dog.entranceexamination_set.all()),
            'treatments': cls.serialize_treatments(dog.treatment_set.all()),
            'observes': cls.serialize_observes(dog.observers.all()),
            'dogPlacements': cls.serialize_dog_placements(dog.dogplacement_set.all()),

        }
        return dog_fields

    @classmethod
    def serialize_dogs(cls, dogs):
        return [cls.serialize_dog(dog) for dog in dogs]
