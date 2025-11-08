package br.com.locadora.view;

import br.com.locadora.data.GerenciadorJogos;
import br.com.locadora.model.Jogo;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class PainelCliente extends JPanel {

    private final GerenciadorJogos gerenciador;
    private final TelaPrincipal telaPrincipal;
    private JTable tabelaJogos;
    private DefaultTableModel modeloTabela;
    private JButton btnAlugar, btnDevolver;
    private JTextField txtBusca;

    // --- Estilo Retrô ---
    private final Color COR_FUNDO = new Color(20, 20, 20);
    private final Color COR_TEXTO = new Color(0, 255, 128);
    private final Color COR_COMPONENTE_FUNDO = new Color(40, 40, 40);
    private final Font FONTE_RETRO = new Font("Monospaced", Font.BOLD, 14);
    // --------------------

    public PainelCliente(GerenciadorJogos gerenciador, TelaPrincipal telaPrincipal) {
        this.gerenciador = gerenciador;
        this.telaPrincipal = telaPrincipal;
        setLayout(new BorderLayout(10, 10));
        setBackground(COR_FUNDO);
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        JPanel painelBusca = criarPainelBusca();
        add(painelBusca, BorderLayout.NORTH);

        criarTabela();
        JScrollPane painelTabela = new JScrollPane(tabelaJogos);
        painelTabela.getViewport().setBackground(COR_FUNDO);
        painelTabela.setBorder(BorderFactory.createLineBorder(COR_TEXTO, 1));
        add(painelTabela, BorderLayout.CENTER);

        criarPainelBotoes();
        atualizarTabela();
    }

    private JPanel criarPainelBusca() {
        JPanel painel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        painel.setBackground(COR_FUNDO);
        painel.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COR_TEXTO), " Buscar Jogo ",
                javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION,
                javax.swing.border.TitledBorder.DEFAULT_POSITION,
                FONTE_RETRO, COR_TEXTO));

        JLabel lblBusca = new JLabel("ID ou Título:");
        lblBusca.setFont(FONTE_RETRO);
        lblBusca.setForeground(COR_TEXTO);

        txtBusca = new JTextField(30);
        txtBusca.setFont(FONTE_RETRO);
        txtBusca.setBackground(COR_COMPONENTE_FUNDO);
        txtBusca.setForeground(COR_TEXTO);
        txtBusca.setCaretColor(COR_TEXTO);
        txtBusca.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(COR_TEXTO, 1),
                BorderFactory.createEmptyBorder(5, 5, 5, 5)));

        JButton btnBuscar = criarBotaoEstilizado("Buscar");
        JButton btnLimparBusca = criarBotaoEstilizado("Mostrar Todos");

        btnBuscar.addActionListener(e -> executarBusca());
        btnLimparBusca.addActionListener(e -> limparBusca());

        painel.add(lblBusca);
        painel.add(txtBusca);
        painel.add(btnBuscar);
        painel.add(btnLimparBusca);
        return painel;
    }

    private void criarPainelBotoes() {
        JPanel painel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
        painel.setBackground(COR_FUNDO);
        btnAlugar = criarBotaoEstilizado("Alugar Jogo Selecionado");
        btnDevolver = criarBotaoEstilizado("Devolver Jogo Selecionado");

        btnAlugar.setEnabled(false);
        btnDevolver.setEnabled(false);

        painel.add(btnAlugar);
        painel.add(btnDevolver);
        add(painel, BorderLayout.SOUTH);

        btnAlugar.addActionListener(e -> alugarJogo());
        btnDevolver.addActionListener(e -> devolverJogo());
    }

    private JButton criarBotaoEstilizado(String texto) {
        JButton button = new JButton(texto);
        button.setFont(FONTE_RETRO);
        button.setBackground(COR_COMPONENTE_FUNDO);
        button.setForeground(COR_TEXTO);
        button.setBorder(BorderFactory.createLineBorder(COR_TEXTO, 1));
        return button;
    }

    private void criarTabela() {
        String[] colunas = {"ID", "Título", "Plataforma", "Gênero", "Status"};
        modeloTabela = new DefaultTableModel(colunas, 0) {
            @Override public boolean isCellEditable(int row, int column) { return false; }
        };
        tabelaJogos = new JTable(modeloTabela);
        estilizarTabela();

        tabelaJogos.getSelectionModel().addListSelectionListener(e -> {
            int linhaSelecionada = tabelaJogos.getSelectedRow();
            if (linhaSelecionada != -1) {
                String status = (String) modeloTabela.getValueAt(linhaSelecionada, 4);
                if (status.equals("Disponível")) {
                    btnAlugar.setEnabled(true);
                    btnDevolver.setEnabled(false);
                } else {
                    btnAlugar.setEnabled(false);
                    btnDevolver.setEnabled(true);
                }
            } else {
                btnAlugar.setEnabled(false);
                btnDevolver.setEnabled(false);
            }
        });
    }

    private void estilizarTabela() {
        tabelaJogos.setBackground(COR_COMPONENTE_FUNDO);
        tabelaJogos.setForeground(COR_TEXTO);
        tabelaJogos.setFont(FONTE_RETRO);
        tabelaJogos.setGridColor(COR_TEXTO.darker());
        tabelaJogos.setSelectionBackground(COR_TEXTO);
        tabelaJogos.setSelectionForeground(COR_COMPONENTE_FUNDO);
        tabelaJogos.getTableHeader().setFont(FONTE_RETRO);
        tabelaJogos.getTableHeader().setBackground(COR_FUNDO);
        tabelaJogos.getTableHeader().setForeground(COR_TEXTO);
    }

    public void atualizarTabela() {
        int linhaSelecionada = tabelaJogos.getSelectedRow();

        preencherTabela(gerenciador.listarTodos());

        if(linhaSelecionada >= 0 && linhaSelecionada < tabelaJogos.getRowCount()){
            tabelaJogos.setRowSelectionInterval(linhaSelecionada, linhaSelecionada);
        }
    }

    private void preencherTabela(Collection<Jogo> jogos) {
        modeloTabela.setRowCount(0);
        for (Jogo jogo : jogos) {
            modeloTabela.addRow(new Object[]{
                    jogo.getId(),
                    jogo.getTitulo(),
                    jogo.getPlataforma(),
                    jogo.getGenero(),
                    jogo.isDisponivel() ? "Disponível" : "Alugado"
            });
        }
    }

    private void executarBusca() {
        String termo = txtBusca.getText().trim();
        if (termo.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Digite um ID ou um termo para buscar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            // Tenta buscar por ID
            int id = Integer.parseInt(termo);
            gerenciador.buscarJogo(id)
                    .ifPresentOrElse(
                            jogo -> preencherTabela(Collections.singletonList(jogo)),
                            () -> {
                                JOptionPane.showMessageDialog(this, "Nenhum jogo encontrado com o ID: " + id, "Não Encontrado", JOptionPane.INFORMATION_MESSAGE);
                                preencherTabela(Collections.emptyList());
                            });
        } catch (NumberFormatException e) {
            // Se não for número, busca por título
            List<Jogo> resultados = gerenciador.buscarJogosPorTitulo(termo);
            preencherTabela(resultados);
        }
        tabelaJogos.clearSelection();
    }

    private void alugarJogo() {
        int linhaSelecionada = tabelaJogos.getSelectedRow();
        if (linhaSelecionada != -1) {
            int id = (int) modeloTabela.getValueAt(linhaSelecionada, 0);
            if (gerenciador.alugarJogo(id)) {
                JOptionPane.showMessageDialog(this, "Jogo alugado com sucesso!");
                telaPrincipal.atualizarTodasAsTabelas();
            } else {
                JOptionPane.showMessageDialog(this, "Não foi possível alugar o jogo.", "Erro", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void devolverJogo() {
        int linhaSelecionada = tabelaJogos.getSelectedRow();
        if (linhaSelecionada != -1) {
            int id = (int) modeloTabela.getValueAt(linhaSelecionada, 0);
            if (gerenciador.devolverJogo(id)) {
                JOptionPane.showMessageDialog(this, "Jogo devolvido com sucesso!");
                telaPrincipal.atualizarTodasAsTabelas();
            } else {
                JOptionPane.showMessageDialog(this, "Não foi possível devolver o jogo.", "Erro", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void limparBusca() {
        txtBusca.setText("");
        atualizarTabela();
    }
}