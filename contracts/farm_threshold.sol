pragma solidity ^0.7.4;

contract farm_threshold {
    
    struct Fruit {
        string fruitName;
        uint256 temperature;
        uint256 weight;
        uint256 noOfDays;
        bool flag;
        uint256 price;
    }
    
    mapping(address => mapping(uint => Fruit)) public fruitArray;
    
    function addFruit(uint _id, string memory _fruitName, uint _temperature, uint _weight, uint _noOfDays, bool _flag, uint _price) public {
        fruitArray[msg.sender][_id] = Fruit(_fruitName, _temperature, _weight, _noOfDays, _flag, _price);
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
            return("Food is spoiled");
        }
        else {
            return("Food is good");
        }
    }
}