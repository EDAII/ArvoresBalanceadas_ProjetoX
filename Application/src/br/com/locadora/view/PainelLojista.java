package br.com.locadora.view;

import br.com.locadora.data.GerenciadorJogos;
import br.com.locadora.model.Jogo;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Collection;

public class PainelLojista extends JPanel {

    private final GerenciadorJogos gerenciador;
    private final TelaPrincipal telaPrincipal;
    private JTable tabelaJogos;
    private DefaultTableModel modeloTabela;

    private JTextField txtId;
    private JTextField txtTitulo;
    private JTextField txtPlataforma;
    private JTextField txtGenero;

    // --- Estilo Retrô ---
    private final Color COR_FUNDO = new Color(20, 20, 20);
    private final Color COR_TEXTO = new Color(0, 255, 128);
    private final Color COR_COMPONENTE_FUNDO = new Color(40, 40, 40);
    private final Font FONTE_RETRO = new Font("Monospaced", Font.BOLD, 14);
    // --------------------

    public PainelLojista(GerenciadorJogos gerenciador, TelaPrincipal telaPrincipal) {
        this.gerenciador = gerenciador;
        this.telaPrincipal = telaPrincipal;
        setLayout(new BorderLayout(10, 10));
        setBackground(COR_FUNDO);
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        criarTabela();
        JScrollPane painelTabela = new JScrollPane(tabelaJogos);
        painelTabela.getViewport().setBackground(COR_FUNDO);
        painelTabela.setBorder(BorderFactory.createLineBorder(COR_TEXTO, 1));
        add(painelTabela, BorderLayout.CENTER);

        JPanel painelFormulario = criarPainelFormulario();
        add(painelFormulario, BorderLayout.EAST);

        JPanel painelSistema = criarPainelSistema();
        add(painelSistema, BorderLayout.SOUTH);

        atualizarTabela();
    }

    private JPanel criarPainelFormulario() {
        JPanel painel = new JPanel();
        painel.setLayout(new BoxLayout(painel, BoxLayout.Y_AXIS));
        painel.setBackground(COR_FUNDO);
        painel.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COR_TEXTO), " Gerenciar Jogo ",
                javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION,
                javax.swing.border.TitledBorder.DEFAULT_POSITION,
                FONTE_RETRO, COR_TEXTO));

        txtId = criarTextFieldEstilizado(15);
        txtTitulo = criarTextFieldEstilizado(15);
        txtPlataforma = criarTextFieldEstilizado(15);
        txtGenero = criarTextFieldEstilizado(15);

        txtId.setEditable(false);
        txtId.setBackground(new Color(50, 50, 50));
        txtId.setText("<Automático>");

        JPanel form = new JPanel(new GridBagLayout());
        form.setBackground(COR_FUNDO);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.anchor = GridBagConstraints.WEST;

        gbc.gridx = 0; gbc.gridy = 0; form.add(criarLabelEstilizado("ID:"), gbc);
        gbc.gridx = 1; gbc.gridy = 0; form.add(txtId, gbc);
        gbc.gridx = 0; gbc.gridy = 1; form.add(criarLabelEstilizado("Título:"), gbc);
        gbc.gridx = 1; gbc.gridy = 1; form.add(txtTitulo, gbc);
        gbc.gridx = 0; gbc.gridy = 2; form.add(criarLabelEstilizado("Plataforma:"), gbc);
        gbc.gridx = 1; gbc.gridy = 2; form.add(txtPlataforma, gbc);
        gbc.gridx = 0; gbc.gridy = 3; form.add(criarLabelEstilizado("Gênero:"), gbc);
        gbc.gridx = 1; gbc.gridy = 3; form.add(txtGenero, gbc);

        JButton btnAdicionar = criarBotaoEstilizado("Adicionar");
        JButton btnAtualizar = criarBotaoEstilizado("Atualizar");
        JButton btnRemover = criarBotaoEstilizado("Remover");
        JButton btnLimpar = criarBotaoEstilizado("Limpar Campos");

        JPanel painelBotoes = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));
        painelBotoes.setBackground(COR_FUNDO);
        painelBotoes.add(btnAdicionar);
        painelBotoes.add(btnAtualizar);
        painelBotoes.add(btnRemover);
        painelBotoes.add(btnLimpar);

        painel.add(form);
        painel.add(Box.createVerticalStrut(10));
        painel.add(painelBotoes);

        btnAdicionar.addActionListener(e -> adicionarJogo());
        btnAtualizar.addActionListener(e -> atualizarJogo());
        btnRemover.addActionListener(e -> removerJogo());
        btnLimpar.addActionListener(e -> limparCampos());

        return painel;
    }

    private JPanel criarPainelSistema() {
        JPanel painel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        painel.setBackground(COR_FUNDO);
        painel.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COR_TEXTO), " Sistema ",
                javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION,
                javax.swing.border.TitledBorder.DEFAULT_POSITION,
                FONTE_RETRO, COR_TEXTO));

        JButton btnAbrirAreaCliente = criarBotaoEstilizado("Abrir Área do Cliente");
        JButton btnGerarBackup = criarBotaoEstilizado("Gerar Backup");
        JButton btnCarregarBackup = criarBotaoEstilizado("Carregar Backup");

        btnAbrirAreaCliente.addActionListener(e -> telaPrincipal.abrirAreaCliente());
        btnGerarBackup.addActionListener(e -> gerarBackup());
        btnCarregarBackup.addActionListener(e -> carregarBackup());

        painel.add(btnAbrirAreaCliente);
        painel.add(btnGerarBackup);
        painel.add(btnCarregarBackup);
        return painel;
    }

    private JLabel criarLabelEstilizado(String texto) {
        JLabel label = new JLabel(texto);
        label.setFont(FONTE_RETRO);
        label.setForeground(COR_TEXTO);
        return label;
    }

    private JTextField criarTextFieldEstilizado(int size) {
        JTextField textField = new JTextField(size);
        textField.setFont(FONTE_RETRO);
        textField.setBackground(COR_COMPONENTE_FUNDO);
        textField.setForeground(COR_TEXTO);
        textField.setCaretColor(COR_TEXTO);
        textField.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(COR_TEXTO, 1),
                BorderFactory.createEmptyBorder(5, 5, 5, 5)));
        return textField;
    }

    private JButton criarBotaoEstilizado(String texto) {
        JButton button = new JButton(texto);
        button.setFont(FONTE_RETRO);
        button.setBackground(COR_COMPONENTE_FUNDO);
        button.setForeground(COR_TEXTO);
        button.setBorder(BorderFactory.createLineBorder(COR_TEXTO, 1));
        return button;
    }

    public void atualizarTabela() {
        modeloTabela.setRowCount(0);
        Collection<Jogo> jogos = gerenciador.listarTodos();
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

    private void criarTabela() {
        String[] colunas = {"ID", "Título", "Plataforma", "Gênero", "Status"};
        modeloTabela = new DefaultTableModel(colunas, 0) {
            @Override public boolean isCellEditable(int row, int column) { return false; }
        };
        tabelaJogos = new JTable(modeloTabela);
        estilizarTabela();
        tabelaJogos.getSelectionModel().addListSelectionListener(event -> {
            if (!event.getValueIsAdjusting() && tabelaJogos.getSelectedRow() != -1) {
                preencherFormularioComLinhaSelecionada();
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

    private void preencherFormularioComLinhaSelecionada() {
        int linhaSelecionada = tabelaJogos.getSelectedRow();
        if (linhaSelecionada != -1) {
            txtId.setText(modeloTabela.getValueAt(linhaSelecionada, 0).toString());
            txtTitulo.setText(modeloTabela.getValueAt(linhaSelecionada, 1).toString());
            txtPlataforma.setText(modeloTabela.getValueAt(linhaSelecionada, 2).toString());
            txtGenero.setText(modeloTabela.getValueAt(linhaSelecionada, 3).toString());
        }
    }

    private void limparCampos() {
        txtId.setText("<Automático>");
        txtTitulo.setText("");
        txtPlataforma.setText("");
        txtGenero.setText("");
        tabelaJogos.clearSelection();
    }

    private void adicionarJogo() {
        String titulo = txtTitulo.getText();
        String plataforma = txtPlataforma.getText();
        String genero = txtGenero.getText();

        if (titulo.isEmpty() || plataforma.isEmpty() || genero.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Todos os campos (exceto ID) devem ser preenchidos.", "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        }

        gerenciador.adicionarJogo(titulo, plataforma, genero);
        telaPrincipal.atualizarTodasAsTabelas();

        limparCampos();
    }

    private void atualizarJogo() {
        try {
            int linhaSelecionada = tabelaJogos.getSelectedRow();
            int id = Integer.parseInt(txtId.getText());
            Jogo jogoAtualizado = new Jogo(id, txtTitulo.getText(), txtPlataforma.getText(), txtGenero.getText());
            gerenciador.buscarJogo(id).ifPresent(jogoAntigo -> jogoAtualizado.setDisponivel(jogoAntigo.isDisponivel()));
            gerenciador.atualizarJogo(jogoAtualizado);

            telaPrincipal.atualizarTodasAsTabelas();
            // Restaura a seleção na tabela
            if (linhaSelecionada != -1 && linhaSelecionada < tabelaJogos.getRowCount()) {
                tabelaJogos.setRowSelectionInterval(linhaSelecionada, linhaSelecionada);
            }

            limparCampos();
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Selecione um item da tabela para atualizar.", "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void removerJogo() {
        int linhaSelecionada = tabelaJogos.getSelectedRow();
        if (linhaSelecionada != -1) {
            int id = (int) modeloTabela.getValueAt(linhaSelecionada, 0);
            int confirmacao = JOptionPane.showConfirmDialog(this, "Tem certeza que deseja remover o jogo permanentemente?", "Confirmação", JOptionPane.YES_NO_OPTION);
            if (confirmacao == JOptionPane.YES_OPTION) {
                gerenciador.removerJogo(id);
                telaPrincipal.atualizarTodasAsTabelas();
                limparCampos();
            }
        } else {
            JOptionPane.showMessageDialog(this, "Selecione um item da tabela para remover.", "Aviso", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void gerarBackup() {
        JFileChooser seletorArquivo = new JFileChooser();
        seletorArquivo.setDialogTitle("Salvar Backup");
        seletorArquivo.setSelectedFile(new File("jogos_backup.dat"));
        seletorArquivo.setFileFilter(new FileNameExtensionFilter("Arquivo de Dados (*.dat)", "dat"));

        int userSelection = seletorArquivo.showSaveDialog(this);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File arquivoParaSalvar = seletorArquivo.getSelectedFile();
            try {
                gerenciador.gerarBackup(arquivoParaSalvar.getAbsolutePath());
                JOptionPane.showMessageDialog(this, "Backup gerado com sucesso!", "Sucesso", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Erro ao gerar backup: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void carregarBackup() {
        JFileChooser seletorArquivo = new JFileChooser();
        seletorArquivo.setDialogTitle("Carregar Backup");
        seletorArquivo.setFileFilter(new FileNameExtensionFilter("Arquivo de Dados (*.dat)", "dat"));

        int userSelection = seletorArquivo.showOpenDialog(this);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File arquivoParaCarregar = seletorArquivo.getSelectedFile();
            try {
                gerenciador.carregarBackup(arquivoParaCarregar.getAbsolutePath());
                telaPrincipal.atualizarTodasAsTabelas();
                JOptionPane.showMessageDialog(this, "Backup carregado com sucesso!", "Sucesso", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException | ClassNotFoundException ex) {
                JOptionPane.showMessageDialog(this, "Erro ao carregar backup: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}