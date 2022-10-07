package com.rainerhahnekamp.news.repository;

import com.rainerhahnekamp.news.entity.EpisodeEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EpisodeRepository extends JpaRepository<EpisodeEntity, Long> {
}
