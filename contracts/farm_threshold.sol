pragma solidity ^0.7.4;

contract farm_threshold {
    
    struct Fruit{
        string fruitName;
        uint256 temperature;
        uint256 weight;
        uint256 noOfDays;
        bool flag;
        string price;
    }
    
    mapping(address => mapping(uint => Fruit)) public fruitArray;
    
    function addFruit(uint _id, string memory _fruitName, uint _temperature, uint _weight, uint _noOfDays, string memory _price) public {
        fruitArray[msg.sender][_id] = Fruit(_fruitName, _temperature, _weight, _noOfDays, true, _price);
    }

     function threshold_value_checking(uint _id, uint _expiryDays) public {
        if(fruitArray[msg.sender][_id].temperature >= 40) {
            fruitArray[msg.sender][_id].flag = false;
        }
        if(fruitArray[msg.sender][_id].weight > 30 && fruitArray[msg.sender][_id].weight < 28) {
            fruitArray[msg.sender][_id].flag = false;
        }
        if(_expiryDays >= fruitArray[msg.sender][_id].noOfDays) {
            fruitArray[msg.sender][_id].flag = false;
        }
    }
    
    function output(uint _id) public view returns(string memory) {
        if(fruitArray[msg.sender][_id].flag == false) {
            return string(abi.encodePacked("Food is spoiled.", " Price is ", fruitArray[msg.sender][_id].price));
        }
        else {
            return string(abi.encodePacked("Food is good.", " Price is ", fruitArray[msg.sender][_id].price));
        }   
    }
}