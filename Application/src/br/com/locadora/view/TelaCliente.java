package br.com.locadora.view;

import br.com.locadora.data.GerenciadorJogos;

import javax.swing.*;
import java.awt.*;

public class TelaCliente extends JFrame {

    private final PainelCliente painelCliente;

    public TelaCliente(GerenciadorJogos gerenciador, TelaPrincipal telaPrincipal) {
        super("Área do Cliente");

        // --- Estilo Retrô ---
        Color fundo = new Color(20, 20, 20);
        getContentPane().setBackground(fundo);
        // --------------------

        // DISPOSE_ON_CLOSE apenas fecha esta janela, não a aplicação inteira.
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(800, 550);
        setLocationRelativeTo(null); // Centraliza na tela

        painelCliente = new PainelCliente(gerenciador, telaPrincipal);
        add(painelCliente);
    }

    public void atualizarTabela() {
        painelCliente.atualizarTabela();
    }
}