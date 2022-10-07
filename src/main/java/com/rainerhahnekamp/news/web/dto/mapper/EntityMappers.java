package com.rainerhahnekamp.news.web.dto.mapper;

import com.rainerhahnekamp.news.entity.EpisodeEntity;
import com.rainerhahnekamp.news.web.dto.Episode;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface EntityMappers {
    Episode toEpisode(EpisodeEntity entity);
    EpisodeEntity fromEpisode(Episode episode);
}
