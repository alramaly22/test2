const themeButton = document.getElementById('theme-button');
const logoImage = document.getElementById('logo');
const darkTheme = 'dark-theme';
const iconTheme = 'uil-sun';

// Previously selected theme (if user selected)
const selectedTheme = localStorage.getItem('selected-theme');
const selectedIcon = localStorage.getItem('selected-icon');

// Obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () =>
  document.body.classList.contains(darkTheme) ? 'dark' : 'light';
const getCurrentIcon = () =>
  themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun';

// Validate if the user previously chose a theme
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark theme
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme);
  themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme);
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
  // Add or remove the dark / icon theme
  document.body.classList.toggle(darkTheme);
  themeButton.classList.toggle(iconTheme);
  // Save the theme and the current icon that the user chose
  localStorage.setItem('selected-theme', getCurrentTheme());
  localStorage.setItem('selected-icon', getCurrentIcon());
});


let lang = {
    ar: {
        subscr: "اشترك الآن",
        prih2:" أسعارنا",
        pris1:"٦٠٠/ج.م",
        pris2:"12/أسبوعًا",
        pris3:"٢٠٠٠/ج.م",
        pris4:"12/أسبوعًا",
        pris5:"٢٥٠٠/ج.م",
        pris6:"12/أسبوعًا",

         prisbr:"أساسي",
        prisbas:"توفير",
        prisp1:"خطة تغذية مخصصة",
        prisp2:"كتاب تمارين مصحوب بشرح فيديوهات",
        prisp3:"كتاب الطهي",
        prisp4:"فحوصات وتغيير الخطط شهريًا عبر البريد الإلكتروني",
        prisp5:"لا متابعة",

        prisilv:"احترافي",
        pripr:"فضي",
        prisilvep1:"خطة تغذية مخصصة",
        prisilvep2:"كتاب تمارين مصحوب بشرح فيديوهات",
        prisilvep3:"كتاب الطهي",
        prisilvep4:"فحوصات وتغيير الخطط كل 14 يومًا",
        prisilvep5:"متابعة يوم بيوم مع الكابتن عاصم التميمي",

        prigold:"اسطوري",
        prient:" ذهبي",
        prisgold1:"خطة تغذية مخصصة",
        prisgold2:"كتاب تمارين مصحوب بشرح فيديوهات",
        prisgold3:"كتاب الطهي",
        prisgold4:"فحوصات وتغيير الخطط أسبوعيًا",
        prisgold5:"متابعة يومية مع الكابتن عاصم التميمي",
        prisgold6:"5 مكالمات هاتفية في الأسبوع مع الكابتن عاصم التميمي",
        footp:"عاصم التميمي هو مدرب لياقة بدنية وخبير تغذية معتمد يمثل رمزاً للتحفيز والتغيير الإيجابي. بفضل خبرته الطويلة في مجال اللياقة البدنية والتغذية، يعمل عاصم  جاهداً على مساعدة الأشخاص في تحقيق أهدافهم الصحية واللياقية. برامجه المخصصة تتيح للعملاء فرصة تحسين صحتهم وتحقيق توازن أفضل في حياتهم. انضموا إليه واستعدوا لبناء نمط حياة أكثر صحة ونشاطًا",

        footh31:"القائمة الرئيسية",
        footha311:"الصفحة الرئيسية",
        footha312:"الفيديوهات",
        footah313:"الأسعار",
        footah314:"التحول",
        footah315:"التذييل",
        footh32:"المعلومات",
        footh321:"الأسئلة الشائعة",
        footh322:"حولنا",
        footh323:"البداية",
        footh324:"البرنامج",
        footh34:"قائمة التواصل الاجتماعي"
  
    },
    en: {
        subscr: "Subscribe Now",
        prih2:"Pricing & Plans",
        pris1:"£/600",
        pris2:"12/weeks",
        pris3:"£/2000",
        pris4:"12/weeks",
        pris5:"£/2500",
        pris6:"12/weeks",


        prisbr:"Basic ",
        prisbas:"Saved",
        prisp1:"Custom nutrition plan",
        prisp2:"Workout e-book explained by videos",
        prisp3:"Cooking e-book",
        prisp4:"Check ins & change plans monthly with email",
        prisp5:"No follow up",

        prisilv:"Professional ",
        pripr:"Silver",
        prisilvep1:"Custom nutrition plan",
        prisilvep2:"Workout e-book explained by videos",
        prisilvep3:"Cooking e-book",
        prisilvep4:"Check ins & change plans 14 days",
        prisilvep5:"Day by day follow up with Captain Assem",

        prigold:"legendary",
        prient:" Gold",
        prisgold1:"Custom nutrition plan",
        prisgold2:"Workout e-book explained by videos",
        prisgold3:"Cooking e-book",
        prisgold4:"Check ins & change plans weekly",
        prisgold5:"Daily follow up with captain Assem",
        prisgold6:"5 times per week phone call with captain Assem",
        footp:"Meet Assem altamimy, a certified fitness trainer and nutrition expert who embodies motivation and positive change. With his extensive experience in the fitness and nutrition field, Qasim is dedicated to helping individuals achieve their health and fitness goals. His personalized programs offer clients the opportunity to improve their health and find better balance in their lives. Join him and get ready to build a healthier, more active lifestyle.",
        footh31:"Main Menu",
        footha311:"Home",
        footha312:"Videos",
        footah313:"Pricing",
        footah314:"Transforamtion",
        footah315:"Footer",
        footh32:"Information",
        footh321:"Faq",
        footh322:"About",
        footh323:"Start",
        footh324:"Program", 
        footh34:"Socail Menu"
    }
};

let selector = document.getElementById('language-selector');

// استدعاء الدالة عند تغيير اللغة
selector.addEventListener('change', updateLanguage);

function updateLanguage() {
    let language = selector.value; // اللغة المختارة
    let nodes = document.querySelectorAll('[data-lang]');

    // تحديث نصوص العناصر باستخدام اللغة المناسبة
    nodes.forEach(node => {
        let key = node.getAttribute('data-lang');
        if (lang[language] && lang[language][key]) {
            node.textContent = lang[language][key];
        }
    });
}

// استدعاء الدالة لتعيين اللغة الافتراضية عند تحميل الصفحة
updateLanguage();

function updateLanguage() {
    let language = selector.value; // اللغة المختارة
    let nodes = document.querySelectorAll('[data-lang]');

    // تحديث نصوص العناصر وتبديل الفئات الخاصة بـ font-family
    nodes.forEach(node => {
        let key = node.getAttribute('data-lang');
        if (lang[language] && lang[language][key]) {
            node.textContent = lang[language][key];
        }

        if (language === 'ar') {
            node.classList.remove('english-font');
            node.classList.add('arabic-font');
        } else {
            node.classList.remove('arabic-font');
            node.classList.add('english-font');
        }

        // إضافة الفئة الإضافية هنا (مثل 'second-arabic-font') إذا كان ذلك مطلوبًا
        // وتبديلها بناءً على اللغة المحددة بنفس الطريقة
        if (language === 'ar') {
            node.classList.remove('english-font');
            node.classList.add('second-arabic-font');
        } else {
            node.classList.remove('second-arabic-font');
            node.classList.add('english-font');
        }
        if (language === 'ar') {
            node.classList.remove('english-font');
            node.classList.add('se-arab');
        } else {
            node.classList.remove('se-arab');
            node.classList.add('english-font');
        }
    });
}


