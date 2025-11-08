package br.com.locadora.model;

import java.io.Serializable;

public class Jogo implements Serializable {

    private static final long serialVersionUID = 1L;

    private int id;
    private String titulo;
    private String plataforma;
    private String genero;
    private boolean disponivel;

    public Jogo(int id, String titulo, String plataforma, String genero) {
        this.id = id;
        this.titulo = titulo;
        this.plataforma = plataforma;
        this.genero = genero;
        this.disponivel = true;
    }

    public int getId() { return id; }

    public void setId(int id) { this.id = id; }

    public String getTitulo() { return titulo; }

    public void setTitulo(String titulo) { this.titulo = titulo; }

    public String getPlataforma() { return plataforma; }

    public void setPlataforma(String plataforma) { this.plataforma = plataforma; }

    public String getGenero() { return genero; }

    public void setGenero(String genero) { this.genero = genero; }

    public boolean isDisponivel() { return disponivel; }

    public void setDisponivel(boolean disponivel) { this.disponivel = disponivel; }

    @Override
    public String toString() {
        return "Jogo{id=" + id + ", titulo='" + titulo + "'}";
    }
}