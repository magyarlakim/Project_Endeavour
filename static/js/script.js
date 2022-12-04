// Functions Calling Other Functions
function cutFruitPieces(fruit) {
    return fruit * 4;
  }
  
function fruitProcessor(apples, oranges) {
    const applePieces = cutFruitPieces(apples);
    const orangePieces = cutFruitPieces(oranges);
  
    const juice = `Juice with ${applePieces} piece of apple and ${orangePieces} pieces of orange.`;
    return juice;
  }
console.log(fruitProcessor(2, 3));
console.log(cutFruitPieces(6));

const calcAge = function(birthYear){
  return 2022 - birthYear;
}

const yearsUntilRetirement = function (birthYear, firstName) {
  const age = calcAge(birthYear);
  const retirement = 65 - age;


  if (retirement > 0) {
    console.log(`${firstName} retires in ${retirement} years`);
    document.getElementById('content').innerHTML = `${firstName} retires in ${retirement} years`
    return retirement;
  } else {
    console.log(`${firstName} has already retired 🎉`);
    document.getElementById('content').innerHTML = `${firstName} has already retired 🎉`
    return -1;
  }
}

// updated function with ability to change

const yearsUntilRetirement_mod = function (firstName) {
  const birthYear = document.getElementById('birthYearRange').value;
  
  //alert(birthYear);
  const age = calcAge(birthYear);
  //alert(age);
  const retirement = 65 - age;

  if (retirement > 0) {
    console.log(`${firstName} retires in ${retirement} years`);
    document.getElementById('content').innerHTML = `${firstName} retire in ${retirement} years`
    return retirement;
  } else {
    console.log(`${firstName} has already retired 🎉`);
    document.getElementById('content').innerHTML = `${firstName} have already retired 🎉`
    return -1;
  }
}

const get_portfolio_type = function(){
  const birthYear = document.getElementById('birthYearRange').value;
  const Notional= 1000000
  //calculate Age;
  const age = calcAge(birthYear);
  // feed in the preference
  const preference = document.getElementById('temp').value;

  if ( age>50 && preference<20) {
    portfolio_proceeds= Notional*1.03
  } else {
    portfolio_proceeds= Notional*2
  }
  document.getElementById('portfolio_proceeds').innerHTML= `FV is:  ${portfolio_proceeds}.`;
  return portfolio_proceeds
}
//console.log(yearsUntilRetirement(1991, 'Jonas'));
//console.log(yearsUntilRetirement(1950, 'Mike'));
//document.getElementById('content').innerHTML = "trial";

const friends = ['Michael', 'Steve', 'Pete'];
const year = new Array(1991, 2022,2034, 2045);
console.log(year[0]);
console.log(year.length);
console.log(friends.length-1);

friends[2] = 'Jay';
// add elemenets
const jonas = ['Jonas', 'Bela', 2037-1990, friends];
friends.push('Jerry');
console.log(friends);
friends.unshift('John');

//remove elements

// pop removes last element
friends.pop(); //last
friends.shift(); //first
console.log(friends.indexOf('Steven'));
// include instead of return the index TRue vs False
console.log(friends.includes('Steven'));
