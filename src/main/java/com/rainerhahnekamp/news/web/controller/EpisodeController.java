package com.rainerhahnekamp.news.web.controller;

import com.rainerhahnekamp.news.entity.EpisodeEntity;
import com.rainerhahnekamp.news.repository.EpisodeRepository;
import com.rainerhahnekamp.news.web.dto.Episode;
import com.rainerhahnekamp.news.web.dto.mapper.EntityMappers;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/episode")
public class EpisodeController {
    private final EpisodeRepository repository;
    private final EntityMappers mappers;

    public EpisodeController(EpisodeRepository repository, EntityMappers mappers) {
        this.repository = repository;
        this.mappers = mappers;
    }

    @GetMapping()
    public List<Episode> index() {
        return repository.findAll().stream().map(mappers::toEpisode).toList();
    }

    @PostMapping()
    public void save(@RequestBody Episode episode) {
        EpisodeEntity entity = repository.findById(episode.getId()).orElseThrow();
        entity.setName(episode.getName());
        entity.setContent(episode.getContent());
        repository.save(entity);
    }

    @PutMapping()
    public void add(@RequestBody Episode episode) {
EpisodeEntity entity = mappers.fromEpisode(episode);
repository.save(entity);
    }
}
