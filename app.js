//Blog do Gui - Codificação
//Chamando express do node modules;
const express = require("express")
//Chamando Handlebars para usar páginas HTML;
const handlebars = require("express-handlebars")
//Chamando Body Parser que tem função semelhante a do handlebars, um ajuda o outro;
const bodyParser = require("body-parser")
//Colocando a função express() na constante app;
const app = express()
//Chamando o cod de admin;
const admin = require("./routes/admin")
//Path para usar pastas no node;
const path = require("path")
//Requirindo o banco de dádos, no caso é o mongoDB;
const mongoose = require("mongoose")
//Chamando o módulo sessão para fazer conexão de admin;
const session = require("express-session")
//Chamando flash para auxuliar na segurança junto com sessão;
const flash = require("connect-flash")
//Chamando postagem e a conexão do bd
require("./models/Postagens")
//Passando conexão para costante
const Postagem = mongoose.model("postagens")
//Carregando model de categorias
require("./models/Categoria")
//Colocando em constante
const Categoria = mongoose.model("categorias")
//chamando usuarios
const usuarios = require("./routes/usuario")
//Carregando passport
const passport = require("passport")
//Chamando auth
require("./config/auth")(passport)


//Configs
//Sessão
app.use(session({
  // Chave para gerar uma sessão
  secret: 'root',
  resave: true,
  saveUninitialized: true
}));
//COnfigurando passport
app.use(passport.initialize())
app.use(passport.session())
//Usando função Flash
app.use(flash());

//Middleware
// requisitando, resposta e próximo;
app.use((req, res, next) => {
  // Comando 'locals' para criar variaveis globais
  res.locals.success_msg = req.flash('success_msg');
  res.locals.error_msg = req.flash('error_msg');
  res.locals.error = req.flash("error")
  res.locals.user = req.user || null;
  // Comando 'next();' para permitir que as rotas avancem apos passarem no mdidleware
  next();
});
//BodyParser
app.use(bodyParser.urlencoded({
  extended: true
}))
app.use(bodyParser.json())

//Handlebars
//Forma padrão de usar handlebars, isso facilita em não ter erros;
app.engine('handlebars', handlebars({
  defaultLayout: 'main',
  runtimeOptions: {
    allowProtoPropertiesByDefault: true,
    allowProtoMethodsByDefault: true,
  },
}))
app.set('view engine', 'handlebars')

//mongoose
mongoose.promise = global.promise;
mongoose.connect("///", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useCreateIndex: true,
  useFindAndModify: false
}).then(() => {
  console.log("Conectado krl!!!")
}).catch((err) => {
  console.log("Deu merda aqui, erro: " + err)
})

//Public
app.use(express.static(path.join(__dirname, "public")))

//Rotas
//rotas sem ser admin

app.get("/postagem/:slug", (req, res) => {
  Postagem.findOne({
    slug: req.params.slug
  }).then((postagens) => {
    if (postagens) {
      res.render("postagem/index", {
        postagens: postagens
      })
    } else {
      req.flash("error_msg", "Esta postagem não existe")
      res.redirect("/")
    }
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro interno!")
    res.redirect("/")
  })
})

app.get("/", (req, res) => {
  Postagem.find().populate("categoria").sort({
    data: "desc"
  }).then((postagens) => {
    res.render("index", {
      postagens: postagens
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro interno!!!")
    res.redirect("/404")
  })
})
app.get("/404", (req, res) => {
  res.send("Erro 404")
})
app.get("/post", (req, res) => {
  res.send("Página de postagens")
})

app.get("/categorias", (req, res) => {
  Categoria.find().then((categorias) => {
    res.render("categorias/index", {
      categorias: categorias
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao listar categorias!!!")
    res.redirect("/")
  })
})

app.get("/categorias/:slug", (req, res) => {
  Categoria.findOne({
    slug: req.params.slug
  }).then((categoria) => {

    if (categoria) {

      Postagem.find({
        categoria: categoria._id
      }).then((postagens) => {
        res.render("categorias/postagens", {
          postagens: postagens,
          categoria: categoria
        })
      }).catch((err) => {
        req.flash("error_msg", "Houve ao listar postagens!!!")
        res.redirect("/")
      })
    } else {
      req.flash("error_msg", "Categoria não existe!!!")
      res.redirect("/")
    }
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro interno ao carregar a página desta categoria!!!")
    res.redirect("/")
  })
})

//rota admin
app.use("/usuarios", usuarios)
app.use("/admin", admin)
//Outros
//Porta usada;
const PORT = process.env.PORT || 8081
//sempre no fim o app.listen;
app.listen(PORT, () => {
  console.log("Servidor rodando!");
})
