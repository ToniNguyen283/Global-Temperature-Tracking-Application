# See assignment for class attributes.
# Remember to include docstrings.
# Start with unittests

class LocalRecord:
    def __init__(self, pos, max=None, min=None, precision = 0):
        #Initiate the attributes for single record
        #Variable: position, max temperature, min temperature, and precision for rounding purpose
        self.pos =  (round(pos[0],precision),round(pos[1],precision))
        self.max = max
        self.min = min
        self.precision = precision

    def add_report(self, temp):
        #Update max/min temperature if appropriate
        #If the record has not had any temp, we will initiate a temp for that record
        if self.max is None or temp > self.max:
            self.max = temp
        if self.min is None or temp<self.min:
            self.min = temp
        
    def __eq__(self, other):
        #returns True if two records are for the same position
        return self.pos == other.pos
    
    def __hash__(self):
        #returns a hash for this object based on its position
        return hash(self.pos)

    def __repr__(self):
        #returns the string representation for the single record
        return f"Record(pos={self.pos}, max={self.max}, min={self.min}"

class RecordsMap:
    def __init__(self):
        #initiate the attributes for the collections of reports
        self._location = 70
        self._len=0
        self._L = [[] for i in range (self._location)]
        
    def __len__(self):
        #return the number of key:value pairs stored
        return self._len

    def _find_index (self,pos):
        #return the index that the record should go in, based on hash(position) and number of locations
        return hash((round(pos[0],0),round(pos[1],0)))%self._location

    def add_report(self, pos, temp):
        #updates max and min temperature for the given position as appropriate.
        index = self._find_index(pos)
        for record in self._L[index]:
            if record.pos == (round(pos[0],0),round(pos[1],0)):
                record.add_report(temp)
                return
        self._L[index].append(LocalRecord(pos,temp,temp))
        self._len+=1
        if self._len>=2*self._location:
            self._rehash(self._location*2)

    def __getitem__(self, pos):
        #returns a tuple of (min, max) temperatures for a given position.
        #Raises KeyError if a point corresponding to the specified tuple is not in the mapping
        index = self._find_index(pos)
        for record in self._L[index]:
            if record.pos == (round(pos[0],0),round(pos[1],0)):
                return (record.min,record.max)
        raise KeyError
  
    def __contains__(self, pos): 
        #returns True (False) if a given position is (is not) in this RecordsMap.
        index = self._find_index(pos)
        for record in self._L[index]:
            if record.pos == (round(pos[0],0),round(pos[1],0)):
                return True
        return False

    def _rehash(self, m_new):
        #rehash as number of entries increases.
        new_list = [[] for i in range (m_new)]
        for record in self._L:
            for item in record:
                a = hash(item) % m_new
                new_list[a].append(item)
        self._location=m_new
        self._L=new_list