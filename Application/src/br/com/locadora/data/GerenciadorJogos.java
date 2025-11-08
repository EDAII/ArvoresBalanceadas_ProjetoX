package br.com.locadora.data;

import br.com.locadora.model.Jogo;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class GerenciadorJogos {
    
    private List<Jogo> listaDeJogos;
    private final Comparator<Jogo> comparadorPorId;
    private int proximoId;

    public GerenciadorJogos() {
        this.listaDeJogos = new ArrayList<>();
        this.comparadorPorId = Comparator.comparingInt(Jogo::getId);
        carregarDadosIniciais();
        atualizarProximoId();
    }

    private int buscaBinariaManual(int id) {
        int inicio = 0;
        int fim = listaDeJogos.size() - 1;

        while (inicio <= fim) {
            int meio = inicio + (fim - inicio) / 2;

            Jogo jogoDoMeio = listaDeJogos.get(meio);

            if (jogoDoMeio.getId() == id) {
                return meio;
            }

            if (id < jogoDoMeio.getId()) {
                fim = meio - 1;
            } else {
                inicio = meio + 1;
            }
        }

        return -1;
    }

    private void atualizarProximoId() {
        this.proximoId = listaDeJogos.stream().mapToInt(Jogo::getId).max().orElse(100) + 1;
    }

    public Optional<Jogo> buscarJogo(int id) {
        int index = buscaBinariaManual(id);

        return (index != -1) ? Optional.of(listaDeJogos.get(index)) : Optional.empty();
    }

    public List<Jogo> buscarJogosPorTitulo(String termo) {
        if (termo == null || termo.trim().isEmpty()) {
            return listarTodos();
        }
        String termoLowerCase = termo.toLowerCase();
        return listaDeJogos.stream()
                .filter(jogo -> jogo.getTitulo().toLowerCase().startsWith(termoLowerCase))
                .collect(Collectors.toList());
    }

    public void adicionarJogo(String titulo, String plataforma, String genero) {
        Jogo novoJogo = new Jogo(proximoId++, titulo, plataforma, genero);
        listaDeJogos.add(novoJogo);
        listaDeJogos.sort(comparadorPorId);
    }

    private void carregarDadosIniciais() {

        listaDeJogos.add(new Jogo(101, "The Witcher 3: Wild Hunt", "PC", "RPG"));
        listaDeJogos.add(new Jogo(102, "Red Dead Redemption 2", "PS4", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(103, "The Legend of Zelda: Breath of the Wild", "Switch", "Aventura"));
        listaDeJogos.add(new Jogo(104, "Cyberpunk 2077", "PC", "RPG"));
        listaDeJogos.add(new Jogo(105, "Elden Ring", "PC", "RPG de Ação"));
        listaDeJogos.add(new Jogo(106, "God of War Ragnarök", "PS5", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(107, "Baldur's Gate 3", "PC", "RPG"));
        listaDeJogos.add(new Jogo(108, "Starfield", "Xbox Series X", "RPG"));
        listaDeJogos.add(new Jogo(109, "Hogwarts Legacy", "PS5", "Aventura"));
        listaDeJogos.add(new Jogo(110, "Marvel's Spider-Man 2", "PS5", "Ação"));
        listaDeJogos.add(new Jogo(111, "Super Mario Bros. Wonder", "Switch", "Plataforma"));
        listaDeJogos.add(new Jogo(112, "Final Fantasy VII Rebirth", "PS5", "RPG"));
        listaDeJogos.add(new Jogo(113, "Street Fighter 6", "PC", "Luta"));
        listaDeJogos.add(new Jogo(114, "Diablo IV", "PC", "RPG de Ação"));
        listaDeJogos.add(new Jogo(115, "Resident Evil 4", "PS5", "Survival Horror"));
        listaDeJogos.add(new Jogo(116, "Alan Wake 2", "PC", "Survival Horror"));
        listaDeJogos.add(new Jogo(117, "Lies of P", "PC", "Souls-like"));
        listaDeJogos.add(new Jogo(118, "Sea of Stars", "Switch", "RPG"));
        listaDeJogos.add(new Jogo(119, "Dave the Diver", "PC", "Aventura"));
        listaDeJogos.add(new Jogo(120, "Hades", "PC", "Roguelike"));
        listaDeJogos.add(new Jogo(121, "Stardew Valley", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(122, "Hollow Knight", "Switch", "Metroidvania"));
        listaDeJogos.add(new Jogo(123, "Celeste", "PC", "Plataforma"));
        listaDeJogos.add(new Jogo(124, "Disco Elysium", "PC", "RPG"));
        listaDeJogos.add(new Jogo(125, "Persona 5 Royal", "PS4", "RPG"));
        listaDeJogos.add(new Jogo(126, "Bloodborne", "PS4", "Souls-like"));
        listaDeJogos.add(new Jogo(127, "Sekiro: Shadows Die Twice", "PC", "Ação"));
        listaDeJogos.add(new Jogo(128, "Ghost of Tsushima", "PS5", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(129, "Horizon Forbidden West", "PS5", "Ação/RPG"));
        listaDeJogos.add(new Jogo(130, "Forza Horizon 5", "Xbox Series X", "Corrida"));
        listaDeJogos.add(new Jogo(131, "Halo Infinite", "Xbox Series X", "FPS"));
        listaDeJogos.add(new Jogo(132, "Gears 5", "Xbox One", "Tiro em Terceira Pessoa"));
        listaDeJogos.add(new Jogo(133, "Animal Crossing: New Horizons", "Switch", "Simulação"));
        listaDeJogos.add(new Jogo(134, "Super Smash Bros. Ultimate", "Switch", "Luta"));
        listaDeJogos.add(new Jogo(135, "Pokémon Legends: Arceus", "Switch", "RPG de Ação"));
        listaDeJogos.add(new Jogo(136, "Metroid Dread", "Switch", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(137, "Death Stranding", "PC", "Ação"));
        listaDeJogos.add(new Jogo(138, "Control", "PC", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(139, "Outer Wilds", "PC", "Aventura"));
        listaDeJogos.add(new Jogo(140, "It Takes Two", "PS5", "Aventura Cooperativa"));
        listaDeJogos.add(new Jogo(141, "Psychonauts 2", "Xbox Series X", "Plataforma"));
        listaDeJogos.add(new Jogo(142, "Ratchet & Clank: Rift Apart", "PS5", "Plataforma"));
        listaDeJogos.add(new Jogo(143, "Returnal", "PS5", "Roguelike"));
        listaDeJogos.add(new Jogo(144, "Sifu", "PS5", "Beat 'em up"));
        listaDeJogos.add(new Jogo(145, "Stray", "PS5", "Aventura"));
        listaDeJogos.add(new Jogo(146, "Tunic", "Xbox Series X", "Aventura"));
        listaDeJogos.add(new Jogo(147, "Vampire Survivors", "PC", "Roguelike"));
        listaDeJogos.add(new Jogo(148, "Xenoblade Chronicles 3", "Switch", "RPG"));
        listaDeJogos.add(new Jogo(149, "The Last of Us Part I", "PS5", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(150, "Uncharted: Legacy of Thieves Collection", "PS5", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(151, "Minecraft", "PC", "Sandbox"));
        listaDeJogos.add(new Jogo(152, "Terraria", "PC", "Sandbox"));
        listaDeJogos.add(new Jogo(153, "Grand Theft Auto V", "PS5", "Ação/Aventura"));
        listaDeJogos.add(new Jogo(154, "Fallout: New Vegas", "PC", "RPG"));
        listaDeJogos.add(new Jogo(155, "The Elder Scrolls V: Skyrim", "PC", "RPG"));
        listaDeJogos.add(new Jogo(156, "Portal 2", "PC", "Puzzle"));
        listaDeJogos.add(new Jogo(157, "Half-Life: Alyx", "PC", "VR/FPS"));
        listaDeJogos.add(new Jogo(158, "BioShock Infinite", "PC", "FPS"));
        listaDeJogos.add(new Jogo(159, "Mass Effect Legendary Edition", "PC", "RPG de Ação"));
        listaDeJogos.add(new Jogo(160, "Dark Souls III", "PC", "Souls-like"));
        listaDeJogos.add(new Jogo(161, "Nier: Automata", "PS4", "RPG de Ação"));
        listaDeJogos.add(new Jogo(162, "Ori and the Will of the Wisps", "Xbox One", "Metroidvania"));
        listaDeJogos.add(new Jogo(163, "Cuphead", "PC", "Run and Gun"));
        listaDeJogos.add(new Jogo(164, "Dead Cells", "Switch", "Roguelike"));
        listaDeJogos.add(new Jogo(165, "Factorio", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(166, "RimWorld", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(167, "Civilization VI", "PC", "Estratégia 4X"));
        listaDeJogos.add(new Jogo(168, "Crusader Kings III", "PC", "Grande Estratégia"));
        listaDeJogos.add(new Jogo(169, "Total War: Warhammer III", "PC", "Estratégia em Tempo Real"));
        listaDeJogos.add(new Jogo(170, "Age of Empires IV", "PC", "Estratégia em Tempo Real"));
        listaDeJogos.add(new Jogo(171, "Valorant", "PC", "FPS Tático"));
        listaDeJogos.add(new Jogo(172, "League of Legends", "PC", "MOBA"));
        listaDeJogos.add(new Jogo(173, "Dota 2", "PC", "MOBA"));
        listaDeJogos.add(new Jogo(174, "Counter-Strike 2", "PC", "FPS Tático"));
        listaDeJogos.add(new Jogo(175, "Apex Legends", "PS5", "Battle Royale"));
        listaDeJogos.add(new Jogo(176, "Fortnite", "PC", "Battle Royale"));
        listaDeJogos.add(new Jogo(177, "Overwatch 2", "PC", "Hero Shooter"));
        listaDeJogos.add(new Jogo(178, "Rocket League", "PC", "Esportes"));
        listaDeJogos.add(new Jogo(179, "FIFA 23", "PS5", "Esportes"));
        listaDeJogos.add(new Jogo(180, "NBA 2K23", "Xbox Series X", "Esportes"));
        listaDeJogos.add(new Jogo(181, "Mortal Kombat 1", "PS5", "Luta"));
        listaDeJogos.add(new Jogo(182, "Guilty Gear -Strive-", "PC", "Luta"));
        listaDeJogos.add(new Jogo(183, "The King of Fighters XV", "PS5", "Luta"));
        listaDeJogos.add(new Jogo(184, "Gran Turismo 7", "PS5", "Corrida/Simulação"));
        listaDeJogos.add(new Jogo(185, "Assetto Corsa Competizione", "PC", "Corrida/Simulação"));
        listaDeJogos.add(new Jogo(186, "F1 23", "PC", "Corrida"));
        listaDeJogos.add(new Jogo(187, "Microsoft Flight Simulator", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(188, "Cities: Skylines II", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(189, "Planet Zoo", "PC", "Simulação"));
        listaDeJogos.add(new Jogo(190, "Jurassic World Evolution 2", "PS5", "Simulação"));
        listaDeJogos.add(new Jogo(191, "No Man's Sky", "PC", "Aventura/Sobrevivência"));
        listaDeJogos.add(new Jogo(192, "Valheim", "PC", "Sobrevivência"));
        listaDeJogos.add(new Jogo(193, "Subnautica", "PC", "Sobrevivência"));
        listaDeJogos.add(new Jogo(194, "The Forest", "PC", "Sobrevivência/Horror"));
        listaDeJogos.add(new Jogo(195, "Phasmophobia", "PC", "Horror"));
        listaDeJogos.add(new Jogo(196, "Among Us", "PC", "Social"));
        listaDeJogos.add(new Jogo(197, "Fall Guys", "PS5", "Party Game"));
        listaDeJogos.add(new Jogo(198, "Jackbox Party Pack 9", "Switch", "Party Game"));
        listaDeJogos.add(new Jogo(199, "Inscryption", "PC", "Card Game/Roguelike"));
        listaDeJogos.add(new Jogo(200, "Slay the Spire", "PC", "Card Game/Roguelike"));
   
        listaDeJogos.sort(comparadorPorId);
    }

    public List<Jogo> listarTodos() {
        return new ArrayList<>(listaDeJogos);
    }

    public void atualizarJogo(Jogo jogoAtualizado) {
        int index = buscaBinariaManual(jogoAtualizado.getId());
        if (index != -1) {
            listaDeJogos.set(index, jogoAtualizado);
        } else {
            System.err.println("Erro: Jogo não encontrado para atualização.");
        }
    }

    public void removerJogo(int id) {
        int index = buscaBinariaManual(id);
        if (index != -1) {
            listaDeJogos.remove(index);
        }
    }

    public boolean alugarJogo(int id) {
        Optional<Jogo> jogoOpt = buscarJogo(id);
        if (jogoOpt.isPresent() && jogoOpt.get().isDisponivel()) {
            jogoOpt.get().setDisponivel(false);
            return true;
        }
        return false;
    }

    public boolean devolverJogo(int id) {
        Optional<Jogo> jogoOpt = buscarJogo(id);
        if (jogoOpt.isPresent() && !jogoOpt.get().isDisponivel()) {
            jogoOpt.get().setDisponivel(true);
            return true;
        }
        return false;
    }

    public void gerarBackup(String caminhoArquivo) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(caminhoArquivo))) {
            oos.writeObject(listaDeJogos);
        }
    }

    @SuppressWarnings("unchecked")
    public void carregarBackup(String caminhoArquivo) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(caminhoArquivo))) {
            List<Jogo> jogosDoBackup = (List<Jogo>) ois.readObject();
            this.listaDeJogos = new ArrayList<>(jogosDoBackup);
            this.listaDeJogos.sort(comparadorPorId);
            atualizarProximoId();
        }
    }
}