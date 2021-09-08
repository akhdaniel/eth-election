pragma solidity 0.4.22;

contract Election2 {
    // Model a Candidate
    struct Candidate {
        uint id;
        string name;
        uint votingSessionId;
        uint voteCount;
    }
    
    //model VoteRecord: voterId sudah milih candidateId mana pada votingSessionId mana
    struct VoteRecord {
        address addr;
        uint votingSessionId;
        uint candidateId;
    }
    VoteRecord[] public voteRecords;
    
    //model Voter
    struct Voter {
        string name;
    }
    uint public voterCount;
    mapping(address => Voter) public voters;
    

    mapping(uint => Candidate) public candidates;
    uint public candidatesCount;

    // voted event
    event votedEvent (
        uint indexed _candidateId
    );

    constructor() public {
        addCandidate("Candidate 1", 1);
        addCandidate("Candidate 2", 1);
        addVoter("Voter 1", 0x53Abd70D632d2C0ba16f1481E37Dee11D45eaB5d);
        addVoter("Voter 2", 0x53144990db4f070c47924E447c4cb9ad52346f2c);
    }

    function addCandidate (string _name, uint _votingSessionId) public {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, _votingSessionId, 0);
    }
    
    function addVoter (string _name, address _addr) public {
        voterCount ++;
        voters[_addr] = Voter(_name);
    }    

    
    function alreadyVote(address _addr, uint _votingSessionId) public constant returns (bool){
        for (uint i=0; i< voteRecords.length; i++ ){
            if (voteRecords[i].addr == _addr && voteRecords[i].votingSessionId == _votingSessionId)
            {
                return true;
            }
        }
        return false;
    }

    function vote (uint _candidateId, address _addr, uint _votingSessionId) public {

        //require valid voter address

        //require that candidate is on the correct voting session
        require(candidates[_candidateId].votingSessionId == _votingSessionId,
            "candidateId not in votingSessionId.");

        // require a valid candidate
        require(_candidateId > 0 && _candidateId <= candidatesCount,
            "candidateId out of range.");

        // require that they haven't voted before
        require(!alreadyVote(_addr, _votingSessionId), 
            "voter alreadyVote in _votingSessionId" );
            
        // record that voter has voted on a _votingSessionId
        voteRecords.push(VoteRecord(_addr, _votingSessionId, _candidateId));

        // update candidate vote Count
        candidates[_candidateId].voteCount ++;

        // trigger voted event
        // votedEvent(_candidateId);
    }
    
    

}
