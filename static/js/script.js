// Functions for the retirnement calculator

const calcAge = function(birthYear) {
  // define the age using current year
  const currentYear = new Date().getFullYear();
  
  if (birthYear) {
    age = currentYear - Number(birthYear);
  } else {
    age = "Please provide valid year";
  }
  return age
};

const yearsUntilRetirement = function (birthYear, firstName) {
  const age = calcAge(birthYear);
  const retirement = 65 - age;


  if (retirement > 0) {
    console.log(`${firstName} retires in ${retirement} years`);
    document.getElementById('content').innerHTML = `${firstName} retires in ${retirement} years`
    return retirement;
  } else {
    console.log(`${firstName} has already retired `);
    document.getElementById('content').innerHTML = `${firstName} has already retired 🎉`
    return -1;
  }
};

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
    document.getElementById('content').innerHTML = `${firstName} have already retired `
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

let countriesContainer = document.querySelector('.countries');

const getCountryData = function(country){
  const request = new XMLHttpRequest();
  request.open('GET',`https://restcountries.com/v3.1/name/${country}`);
  request.send();

  request.addEventListener('load', function(){
    

  const data = JSON.parse(this.responseText)[0];
  //console.log(data);

  let  html_object=
    `<div class="card border-secondary mb-3" style="max-width: 100rem;">
                <div class="card-header">${data.name.official}
                <img class="country_img" src="${data.coatOfArms.png}" height="20" />
                </div>
                <div class="card-body">
                
                <div>
                <ul>
                <li>
                Capital: ${data.capital}
                </li>
                <li>
                Region: ${data.region} 
                </li>
                <li>
                Subregion: ${data.subregion}
                </li>
                </ul>
                </div>
                </div>
      </div>
    `

    //console.log(html_object);
    document.querySelector('.countries').insertAdjacentHTML('beforeend', html_object);
  });
};

const getCountryAndNeigborData = function(country){
  const request = new XMLHttpRequest();
  request.open('GET',`https://restcountries.com/v3.1/name/${country}`);
  request.send();

  request.addEventListener('load', function(){
    

  const data = JSON.parse(this.responseText)[0];
  console.log(data);

  let  html_object=
    `<div class="card border-secondary mb-3" style="max-width: 100rem;">
                <div class="card-header">${data.name.official}
                <img class="country_img" src="${data.coatOfArms.png}" height="20" />
                </div>
                <div class="card-body">
                
                <div>
                <ul>
                <li>
                Capital: ${data.capital}
                </li>
                <li>
                Region: ${data.region} 
                </li>
                <li>
                Subregion: ${data.subregion}
                </li>
                </ul>
                </div>
                </div>
      </div>
    `

    //console.log(html_object);
    document.querySelector('.countries').insertAdjacentHTML('beforeend', html_object);
  });
};
document.addEventListener('DOMContentLoaded', function() {
  get_portfolio_type();
  yearsUntilRetirement_mod('Bélam');
}, false);
getCountryData('usa');
getCountryData('switzerland');
getCountryData('qatar');
getCountryData('hungary');
//getCountryData('serbia');
//getCountryData('russia');

let country= 'russia';

const getCountryDataFetch = function(country){
  fetch(`https://restcountries.com/v3.1/name/${country}`
  ).then(
  function(response) {
    return response.json();
  }
  ).then(
    function(data){
      console.log(data);
    }
  );
};
const getCountryDataFetch_clean = function(country){
  fetch(`https://restcountries.com/v3.1/name/${country}`)
  .then( response => response.json())
  .then( data => console.log(data));
};
getCountryDataFetch('hungary');
getCountryDataFetch_clean('israel');