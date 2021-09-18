const express = require('express')
const router = express.Router()
const mongoose = require("mongoose")
require("../models/Categoria")
const Categoria = mongoose.model("categorias")
require("../models/Postagens")
const Postagem = mongoose.model("postagens")
const {eAdmin} = require("../helpers/eAdmin")

router.get('/',  (req, res) => {
  res.render("admin/index")
})

router.get('/posts', eAdmin, (req, res) => {
  res.send("Página dos posts")
})

router.get('/categorias', eAdmin, (req, res) => {
  Categoria.find().sort({
    date: 'desc'
  }).then((categorias) => {
    res.render("admin/categorias", {
      categorias: categorias
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao listar as categorias")
    res.redirect("/admin")
  })
})

router.get('/categorias/add', eAdmin, (req, res) => {
  res.render("admin/addcategorias")
})

//Inserindo dados do formularios no bd;
router.post("/categorias/nova", eAdmin, (req, res) => {

  //Validação de formularios de nova categoria;
  var erros = []

  if (!req.body.nome || typeof req.body.nome == undefined || req.body.nome == null) {
    erros.push({
      texto: "Nome inválido"
    })
  }
  if (!req.body.slug || typeof req.body.slug == undefined || req.body.slug == null) {
    erros.push({
      texto: "Slug inválido"
    })
  }
  if (req.body.nome.lenght < 2) {
    erros.push({
      texto: "Nome da categoria é muito pequeno"
    })
  }
  if (erros.lenght > 0) {
    res.render("admin/addcategorias", {
      erros: erros
    })
  } else {
    const novaCategoria = {
      nome: req.body.nome,
      slug: req.body.slug
    }

    new Categoria(novaCategoria).save().then(() => {
      req.flash("success_msg", "Categoria criada com sucesso!")
      res.redirect("/admin/categorias")
    }).catch((err) => {
      req.flash("error_msg", "Houve um erro ao salvar categoria, tente novamente!")
      res.redirect("/admin/categorias")
    })
  }
})

router.post("/categorias/edit", eAdmin, (req, res) => {

  //Validação de formularios de editar categoria;
  var erro = []

  if (!req.body.nome || typeof req.body.nome == undefined || req.body.nome == null) {
    erro.push({
      texto: "Nome inválido"
    })
  }
  if (!req.body.slug || typeof req.body.slug == undefined || req.body.slug == null) {
    erro.push({
      texto: "Slug inválido"
    })
  }
  if (req.body.nome.lenght < 2) {
    erro.push({
      texto: "Nome da categoria é muito pequeno"
    })
  }
  if (erro.lenght > 0) {
    res.render("admin/editcategorias", {
      erro: erro
    })
  } else {

    Categoria.findOne({
      _id: req.body.id
    }).then((categoria) => {
      categoria.nome = req.body.nome
      categoria.slug = req.body.slug

      categoria.save().then(() => {
        req.flash("success_msg", "Categoria editada com sucesso!")
        res.redirect("/admin/categorias")
      }).catch((err) => {
        req.flash("error_msg", "Houve um erro ao salvar a categoria")
        res.redirect("/admin/categorias")
      })

    }).catch((err) => {
      req.flash("error_msg", "Houve um erro ao editar categoria")
      res.redirect("/admin/categorias")
    })
  }
})

router.get("/categorias/edit/:id", eAdmin, (req, res) => {
  Categoria.findOne({
    _id: req.params.id
  }).then((categoria) => {
    res.render("admin/editcategorias", {
      categoria: categoria
    })
  }).catch((err) => {
    req.flash("error_msg", "Esta categoria não existe")
    res.redirect("/admin/categorias")
  })

})

router.post("/categorias/deletar", eAdmin, (req, res) => {
  Categoria.remove({
    _id: req.body.id
  }).then(() => {
    req.flash("success_msg", "Categoria excluída com sucesso!")
    res.redirect("/admin/categorias")
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao excluir a categoria")
    res.redirect("/admin/categorias")
  })
})

//Postagem cod de rotas;
router.get("/postagens", eAdmin, (req, res) => {
  Postagem.find().populate("categoria").sort({
    data: "desc"
  }).then((postagens) => {
    res.render("admin/postagens", {
      postagens: postagens
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao listar postagens")
    res.redirect("/admin")
  })

})

router.get("/postagens/add", eAdmin, (req, res) => {
  Categoria.find().then((categorias) => {
    res.render("admin/addpostagens", {
      categorias: categorias
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao carregar o formulário")
    res.redirect("/admin")
  })

})

router.post("/postagens/nova", eAdmin, (req, res) => {
  var erros = []
  if (req.body.categoria == "0") {
    erros.push({
      texto: "Categoria inválida, registre uma categoria"
    })
  }
  if (erros.lenght > 0) {
    res.render("admin/addpostagens", {
      erros: erros
    })

  } else {
    const novaPostagem = {
      titulo: req.body.titulo,
      slug: req.body.slug,
      descricao: req.body.descricao,
      conteudo: req.body.conteudo,
      categoria: req.body.categoria

    }
    new Postagem(novaPostagem).save().then(() => {
      req.flash("success_msg", "Postagem criada com sucesso!")
      res.redirect("/admin/postagens")
    }).catch((err) => {
      req.flash("error_msg", "Houve um erro ao criar  postagem")
      res.redirect("/admin/postagens")
    })

  }
})
router.get("/postagens/edit/:id", eAdmin, (req, res) => {

  Postagem.findOne({
    _id: req.params.id
  }).then((postagem) => {

    Categoria.find().then((categorias) => {
      res.render("admin/editpostagens", {
        categorias: categorias,
        postagem: postagem
      })
    }).catch((err) => {
      req.flash("error_msg", "Houve um erro ao listar as categorias")
      res.redirect("/admin/postagens")
    })
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao carregar o formulário de edição")
    res.redirect("/admin/postagens")
  })
})

router.post("/postagens/edit", eAdmin, (req, res) => {
  Postagem.findOne({
    _id: req.body.id
  }).then((postagem) => {

    postagem.titulo = req.body.titulo,
      postagem.slug = req.body.slug,
      postagem.descricao = req.body.descricao,
      postagem.conteudo = req.body.conteudo,
      postagem.categoria = req.body.categoria

    postagem.save().then(() => {
      req.flash("success_msg", "Postagem editada com sucesso!")
      res.redirect("/admin/postagens")
    }).catch((err) => {
      req.flash("success_msg", "Erro ao editar a postagem")
      res.redirect("/admin/postagens")
    })
  }).catch((err) => {
    req.flash("error_msg", "Erro ao salvar edição!")
    res.redirect("/admin/postagens")
  })
})

router.post("/postagens/deletar", eAdmin, (req, res) => {
  Postagem.deleteOne({
    _id: req.body.id
  }).then(() => {
    req.flash("success_msg", "Postagem excluída com sucesso!")
    res.redirect("/admin/postagens")
  }).catch((err) => {
    req.flash("error_msg", "Houve um erro ao excluir a postagem")
    res.redirect("/admin/postagens")
  })
})
module.exports = router
