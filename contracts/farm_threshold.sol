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
            return string(abi.encodePacked("Food is Spoiled.", " Price is ", fruitArray[msg.sender][_id].price));
        }
        else {
            return string(abi.encodePacked("Food is Good.", " Price is ", fruitArray[msg.sender][_id].price));
        }   
    }
    
    struct asset {
        string asset_name;
        uint day;
        uint month;
        uint year;
        bool flag;
    }
    
    mapping(address => mapping(uint => asset)) public assetArray;
    
    function book_asset(uint _id, string memory _asset_name, uint _day, uint _month, uint _year) public {
        assetArray[msg.sender][_id] = asset(_asset_name, _day, _month, _year, true);
    }
    
    function check_asset(uint _id, uint _day, uint _month, uint _year) public {
        if(assetArray[msg.sender][_id].flag == false) {
            assetArray[msg.sender][_id].flag = true;
        }
        else if(assetArray[msg.sender][_id].day == _day && assetArray[msg.sender][_id].month == _month && assetArray[msg.sender][_id].year == _year) {
            assetArray[msg.sender][_id].flag = false;
        }
    }
    
    function print(uint _id) public view returns(string memory) {
        if(assetArray[msg.sender][_id].flag == false) {
            return string(abi.encodePacked("Asset is booked already by someone"));
        }
        else {
             return string(abi.encodePacked("Successfully Booked"));
        }
        
    }
    
    function print1(uint _id) public view returns(string memory) {
        if(assetArray[msg.sender][_id].flag == false) {
            return string(abi.encodePacked("Asset is booked already by someone"));
        }
        else {
             return string(abi.encodePacked("Available"));
        }
        
    }
}