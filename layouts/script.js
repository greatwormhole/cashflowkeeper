const user=document.querySelector(".user")
const greetings=document.querySelector(".greetings")
const user_name=document.querySelector(".user_name")
const greeting_name=document.querySelector(".greeting_name")
const expense_button=document.querySelector(".expense_button")
const expense_nav = document.querySelector('.expense_nav')

const title=document.querySelector('title')





const example_name = 'Маша';
const example_surname = 'Моргунова';
const example_country = 'Russia';
const example_mail = 'sopids@dklj.com'


const example_history_activity = [
  {
  infoText: 'Clothes',
  image: '../icons/clothes.png',
  date: '06 Jan 2023',
  money: '-$28',
 },
 {
  infoText: 'Transport',
  image: '../icons/transport.png',
  date: '01 Jan 2023',
  money: '-$15',
 },
 {
  infoText: 'Supermarket',
  image: '../icons/supermarket.png',
  date: '06 Jab 2023',
  money: '-$9',
 },
 {
  infoText: 'Entertainment',
  image: '../icons/entertainment.png',
  date: '01 Jan 2023',
  money: '-$4',
 },
 {
  infoText: 'Other',
  image: '../icons/other.png',
  date: '28 Dec 2022',
  money: '-$7',
 }
]

const numbers_examples = {
  incomes: {
    absolute: '$24.400',
    percents: '+2.4'
  },
  outcomes: {
    absolute: '$12.500',
    percents: '+3.5'
  },
  investments: {
    absolute: '$500',
    percents: '-4.6'
  }
}

const example_history_operations = [
  {
  date: '08 Jan 2023',
  category: "Children's products",
  amount: '-$1,79',
  comment: 'Running trainers',
  },
  {
  date: '08 Jan 2023',
  category: "Children's products",
  amount: '-$1,79',
  comment: 'Running trainers',
  },
  {
  date: '08 Jan 2023',
  category: "Children's products",
  amount: '-$1,79',
  comment: 'Running trainers',
  }
]


greeting_name.textContent = example_name;
user_name.textContent = example_name;


user.addEventListener('mouseover', (event) => {
  user_name.style.display = 'block';
  setTimeout(() => {
    user_name.style.display = 'none';
  }, 1500);
});



expense_button.addEventListener('click', (event) => {
  if (expense_nav.style.width == '295px') {
    expense_nav.style.width = '0';
  }
  else {
    expense_nav.style.width = '295px';
  }
})


const cardTemplate = document.querySelector(".recent-block-template");
const section = document.querySelector(".recent-block");

function addActivity(object) {
  const newBlock = cardTemplate.content.cloneNode(true);
  const infoText = newBlock.querySelector(".info-text")
  const date = newBlock.querySelector(".adding-info-annotation")
  const price = newBlock.querySelector(".annotation")
  const image = newBlock.querySelector(".image")
  infoText.textContent = object.infoText;
  date.textContent = object.date
  price.textContent = object.money
  image.src = object.image
  section.prepend(newBlock);
}

example_history_activity.forEach(item => {
  addActivity(item);
})





if (title.textContent == 'Home Page') {
const incomes_number = document.querySelector('.incomes-number')
const outcomes_number = document.querySelector('.outcomes-number')
const investments_number = document.querySelector('.investments-number')
const incomes_percent_number = document.querySelector('.incomes-percent-number')
const outcomes_percent_number = document.querySelector('.outcomes-percent-number')
const investments_percent_number = document.querySelector('.investments-percent-number')

incomes_number.textContent = numbers_examples.incomes.absolute
outcomes_number.textContent = numbers_examples.outcomes.absolute
investments_number.textContent = numbers_examples.investments.absolute

function showPercents(module, percents) {
  if (percents[0]=='+') {
    console.log(percents[0])
    module.style.color = '#1db171'
  }
  else if (percents[0]=='-') {
    module.style.color = 'red'
  }
  else {
    module.style.color = '#212529'
  }
  module.textContent = percents
}
showPercents(incomes_percent_number, numbers_examples.incomes.percents)
showPercents(outcomes_percent_number,  numbers_examples.outcomes.percents)
showPercents(investments_percent_number,  numbers_examples.investments.percents)
}


if (title.textContent == 'Profile And Settings') {
  const info_user_name = document.querySelector('.info_user_name')
  info_user_name.textContent = example_name
  const info_user_surname = document.querySelector('.info_user_surname')
  info_user_surname.textContent = example_surname
  const info_user_country = document.querySelector('.info_user_country')
  info_user_country.textContent = example_country
  const info_user_mail = document.querySelector('.info_user_mail')
  info_user_mail.textContent = example_mail


}


// if (title.textContent == 'History') {
//   const historyRowTemplate = document.querySelector(".operations_history_template");
//   const section = document.querySelector(".full history");

//   function addActivity(object) {
//   const newBlock = historyRowTemplate.content.cloneNode(true);
//   const date_col = newBlock.querySelector(".date_col")
//   const category_col = newBlock.querySelector(".category_col")
//   const amount_col = newBlock.querySelector(".amount_col")
//   const comment_col = newBlock.querySelector(".comment_col")
//   // const delete_button = newBlock.querySelector(".detele_button")
//   date_col.textContent = object.date_col.textContent;
//   category_col.textContent = object.category_col.textContent;
//   amount_col.textContent = object.amount_col.textContent;
//   comment_col.textContent = object.comment_col.textContent;
//   // delete_button = object.delete_button;
//   section.prepend(newBlock);
// }
// }







// src="https://cdn.jsdelivr.net/npm/chart.js"

  // bar chart first run
//   var data_first_run_Income = [];
//   var data_first_run_Outcome = [];

//   var labels_first_run = [];

//   var all_data = [
//   { data_first_run: [ {% for item in transaction %}
//                 {{ item.sum_of_amount }},
//           {% endfor %} ],
//     labels_first_run:  [{% for item in transaction %}
//                  "{{ item.date }}",
//              {% endfor %} ],
//     type: [ {% for item in transaction %}
//                   "{{ item.type }}",
//           {% endfor %} ]
//   }
//   ]

// let flag = 0;

// for (let i=0; i < all_data[0].type.length; i++){
//     if (all_data[0].type[i] == "Income") {
//         data_first_run_Income[i-flag] = all_data[0].data_first_run[i];
//         labels_first_run[i-flag] = all_data[0].labels_first_run[i];
//     } else {
//         flag++
//     }
// }

// let flag_1 = 0;

// for (let i=0; i < all_data[0].type.length; i++){
//     if (all_data[0].type[i] == "Outcome") {
//         data_first_run_Outcome[i-flag_1] = all_data[0].data_first_run[i];
//     } else {
//         flag_1++
//     }
// }


// barchart config

//   var config = {
//     type: 'bar',
//     data: {
//       labels: labels_first_run,
//       datasets: [
//         {
//           label: 'Income',
//           backgroundColor: 'rgba(31, 180, 171, 1)',
//           borderRadius: 30,
//           borderColor: 'lightblue',
//           data: data_first_run_Income,
//           fill: false,
//         },
//         {
//           label: 'Outcome',
//           backgroundColor: 'rgba(217, 94, 94, 1)',
//           borderRadius: 30,
//           borderColor: 'lightblue',
//           data: data_first_run_Outcome,
//           fill: false,
//         }
//       ]
//     },
//     options: {
//       responsive: true
//     }
//   };

// // barchart creating
//   var ctx = document.getElementById('chart').getContext('2d');
//   myChart = new Chart(ctx, config);

// // first_run_date_settings
// filterData();

// // functions

//    function filterData(){
//      var labels2 = [...labels_first_run];
//      console.log(labels2);
//      const startlabel = document.getElementById('startdate');
//      const endlabel = document.getElementById('enddate');

//      // get the index number in array
//      var indexstartlabel = labels2.indexOf(startlabel.value);
//      var indexendlabel = labels2.indexOf(endlabel.value);

//      if (indexstartlabel == -1) {
//        indexstartlabel = 0;
//      }
//      if (indexendlabel == -1) {
//        indexendlabel = labels2.length - 1;
//      }

//      //slice the array
//      const filterDate = labels2.slice(indexstartlabel, indexendlabel + 1);
//      config.data.labels = filterDate;

//      // datapoints
//      const data_Income2 = [...data_first_run_Income];
//      const data_Outcome2 = [...data_first_run_Outcome];
//      const filterDatapoints_1 = data_Income2.slice(indexstartlabel, indexendlabel + 1);
//      const filterDatapoints_2 = data_Outcome2.slice(indexstartlabel, indexendlabel + 1);
//      config.data.datasets[0].data = filterDatapoints_1;
//      config.data.datasets[1].data = filterDatapoints_2;

//      myChart.update();
//    }


