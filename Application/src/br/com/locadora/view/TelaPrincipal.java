package br.com.locadora.view;

import br.com.locadora.data.GerenciadorJogos;

import javax.swing.*;
import java.awt.*;

public class TelaPrincipal extends JFrame {

    private final GerenciadorJogos gerenciador;
    private PainelLojista painelLojista;
    private TelaCliente telaCliente; // Agora é uma janela separada

    public TelaPrincipal() {
        super("Sistema de Aluguel de Jogos");

        // --- Estilo Retrô ---
        Color fundo = new Color(20, 20, 20);
        Color texto = new Color(0, 255, 128);
        UIManager.put("TabbedPane.background", fundo);
        UIManager.put("TabbedPane.foreground", texto);
        // --------------------

        this.gerenciador = new GerenciadorJogos();

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(850, 600);
        setLocationRelativeTo(null);

        JTabbedPane abas = new JTabbedPane();

        painelLojista = new PainelLojista(gerenciador, this);

        abas.addTab("Área do Lojista", painelLojista);

        add(abas);
    }

    // Este método agora atualiza a tabela do lojista e, se a janela do cliente estiver aberta, a dela também.
    public void atualizarTodasAsTabelas() {
        painelLojista.atualizarTabela();
        if (telaCliente != null && telaCliente.isVisible()) {
            telaCliente.atualizarTabela();
        }
    }

    public void abrirAreaCliente() {
        if (telaCliente == null || !telaCliente.isDisplayable()) {
            telaCliente = new TelaCliente(gerenciador, this);
        }
        telaCliente.setVisible(true);
        telaCliente.toFront(); // Traz a janela para frente
    }
}